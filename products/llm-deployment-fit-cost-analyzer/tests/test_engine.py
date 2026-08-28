from src.engine import AnalysisInput, analyze

def test_small_quantized_model_passes():
    r = analyze(AnalysisInput(8,4,24,8192,1))
    assert r["fit"] == "PASS"

def test_mid_model_is_risk():
    r = analyze(AnalysisInput(32,4,24,8192,1))
    assert r["fit"] == "RISK"

def test_large_fp16_model_fails():
    r = analyze(AnalysisInput(70,16,80,8192,1))
    assert r["fit"] == "FAIL"

def test_long_context_forces_benchmark():
    r = analyze(AnalysisInput(8,4,24,32768,1))
    assert r["benchmark_required"] is True

def test_user_supplied_economics():
    r = analyze(AnalysisInput(8,4,24,8192,1,price_per_hour_usd=0.5,hours_per_month=100))
    assert r["economics"]["estimated_monthly_gpu_cost_usd"] == 50.0
