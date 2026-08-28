import asyncio
from apify import Actor
from .engine import AnalysisInput, analyze

async def main():
    async with Actor:
        data = await Actor.get_input() or {}
        required = ["parameter_count_b","quantization_bits","gpu_vram_gb","context_length","concurrency"]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        result = analyze(AnalysisInput(
            parameter_count_b=float(data["parameter_count_b"]),
            quantization_bits=int(data["quantization_bits"]),
            gpu_vram_gb=float(data["gpu_vram_gb"]),
            context_length=int(data["context_length"]),
            concurrency=int(data["concurrency"]),
            architecture_overhead_pct=float(data.get("architecture_overhead_pct",25.0)),
            price_per_hour_usd=(float(data["price_per_hour_usd"]) if data.get("price_per_hour_usd") is not None else None),
            hours_per_month=(float(data["hours_per_month"]) if data.get("hours_per_month") is not None else None),
        ))

        await Actor.push_data(result)
        charge = await Actor.charge(event_name="analysis-completed")
        Actor.log.info(
            "analysis-completed charged_count=%s limit_reached=%s",
            getattr(charge, "charged_count", None),
            getattr(charge, "event_charge_limit_reached", None),
        )
        return

if __name__ == "__main__":
    asyncio.run(main())
