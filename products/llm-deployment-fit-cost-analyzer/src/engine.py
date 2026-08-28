from dataclasses import dataclass
from math import ceil
from typing import Optional

@dataclass
class AnalysisInput:
    parameter_count_b: float
    quantization_bits: int
    gpu_vram_gb: float
    context_length: int
    concurrency: int
    architecture_overhead_pct: float = 25.0
    price_per_hour_usd: Optional[float] = None
    hours_per_month: Optional[float] = None

def analyze(x: AnalysisInput) -> dict:
    if x.quantization_bits not in (4,8,16):
        raise ValueError("quantization_bits must be 4, 8, or 16")
    if x.parameter_count_b <= 0 or x.gpu_vram_gb <= 0:
        raise ValueError("parameter_count_b and gpu_vram_gb must be positive")
    if x.context_length < 512 or x.concurrency < 1:
        raise ValueError("context_length >= 512 and concurrency >= 1 required")

    weight_gb = x.parameter_count_b * (x.quantization_bits / 8.0)
    runtime_reserve_gb = weight_gb * (x.architecture_overhead_pct / 100.0)
    kv_risk_proxy_gb = 0.6 * max(x.context_length / 8192.0, 0.25) * max(float(x.concurrency), 1.0)

    floor_gb = weight_gb + runtime_reserve_gb + kv_risk_proxy_gb
    headroom_gb = x.gpu_vram_gb - floor_gb
    utilization = floor_gb / x.gpu_vram_gb

    if headroom_gb < 0:
        fit, oom_risk = "FAIL", "HIGH"
    elif utilization >= 0.90:
        fit, oom_risk = "RISK", "HIGH"
    elif utilization >= 0.78:
        fit, oom_risk = "RISK", "MEDIUM"
    else:
        fit, oom_risk = "PASS", "LOW"

    benchmark_required = fit != "PASS" or x.context_length >= 32768 or x.concurrency >= 8
    target = max(floor_gb / 0.78, floor_gb + 2.0)
    classes = [16,24,32,48,64,80,96,141,192]
    recommended_class = next((v for v in classes if v >= target), ceil(target))

    economics = {"available": False}
    if x.price_per_hour_usd is not None and x.hours_per_month is not None:
        economics = {
            "available": True,
            "price_per_hour_usd": round(x.price_per_hour_usd,4),
            "hours_per_month": round(x.hours_per_month,2),
            "estimated_monthly_gpu_cost_usd": round(x.price_per_hour_usd * x.hours_per_month,2),
            "note": "User-supplied price; no live provider price lookup performed."
        }

    util_start = 0.85 if fit == "PASS" else 0.78
    next_action = {
        "FAIL":"Use more VRAM, stronger quantization, or multi-GPU; then benchmark.",
        "RISK":"Increase headroom or reduce context/concurrency; benchmark before production.",
        "PASS":"Static fit looks credible; benchmark representative prompts before production."
    }[fit]

    return {
        "fit": fit,
        "oom_risk": oom_risk,
        "estimated_weight_memory_gb": round(weight_gb,2),
        "runtime_reserve_gb": round(runtime_reserve_gb,2),
        "kv_cache_risk_proxy_gb": round(kv_risk_proxy_gb,2),
        "estimated_memory_floor_gb": round(floor_gb,2),
        "candidate_gpu_vram_gb": x.gpu_vram_gb,
        "estimated_headroom_gb": round(headroom_gb,2),
        "recommended_min_vram_class_gb": recommended_class,
        "recommended_vllm_args": {
            "gpu_memory_utilization": util_start,
            "max_model_len": x.context_length,
            "max_num_seqs": max(1,min(x.concurrency,32)),
            "note":"Starting point only; benchmark before production."
        },
        "benchmark_required": benchmark_required,
        "economics": economics,
        "assumptions": [
            "Weight memory is estimated from parameter count and quantization only.",
            "KV-cache is a risk proxy, not architecture-exact.",
            "Exact production sizing requires model metadata and representative benchmarking.",
            "No live provider pricing is used unless explicitly supplied by the caller."
        ],
        "next_action": next_action
    }
