# FORGE.ONE — Runpod AI Test Report

Date: 2026-07-14  
Status: TEST COMPLETE  
Environment: Runpod Pod, NVIDIA RTX A4500 20 GB

## Goal

Test whether a small local language model can act as an evidence-based FORGE.ONE analysis engine without relying on a paid hosted model API.

## What worked

- Runpod API access from Termux
- SSH access with mobile public key
- RTX A4500 GPU and CUDA 12.8
- PyTorch 2.8.0+cu128
- Qwen2.5-3B-Instruct loaded in 4-bit mode
- Structured JSON output
- FORGE.ONE benchmark across multiple ideas
- Stable fact extraction in a three-run guard test

## What failed or required repair

- Initial vLLM install pulled a Torch/CUDA stack that required a newer NVIDIA driver
- The original 20 GB container disk filled during the 7B model download
- Qwen2.5-7B-Instruct was abandoned for this test
- The 3B model occasionally violated enum spelling and invented unsupported evidence before guardrails were added

## Benchmark summary

### FORGE.ONE

- Score: 25
- Verdict: TEST_FIRST
- Main risk: no confirmed completions, repeat users, or payments
- Useful next test: offer five Deep Forge reports for 490 NOK within seven days

### 2LvLUP

- Score: 45
- Verdict: TEST_FIRST
- Main risk: taste, effects, pricing, compliance, and repeat purchase remain unproven
- Failure observed: the model incorrectly upgraded proposed paid preorders into secured paid preorders

### AI motivational wallpaper generator

- Score: 25
- Verdict: TEST_FIRST
- Main risk: no evidence that users will pay for a product with many free substitutes

## Guard test

The same 2LvLUP evidence audit was run three times.

Results:

- Facts stayed stable across all runs
- No payments or preorders were invented
- Possible distribution was not upgraded to confirmed distribution
- The verdict string was misspelled consistently as `HALLULATION_RISK`

## Final engineering verdict

The 3B model is useful as an analysis assistant, but not safe as the only decision-maker.

FORGE.ONE should use a hybrid architecture:

1. Deterministic input and evidence parsing
2. Model analysis and suggestion generation
3. Schema validation
4. Enum validation
5. Evidence-grounding checks
6. Contradiction checks
7. Human-readable verdict generation

## Product conclusion

FORGE.ONE survived as a problem and service test, not yet as a validated SaaS.

Current best reality test:

- Offer: five manually reviewed Deep Forge reports
- Price: 490 NOK each
- Window: seven days
- Success: at least two paid reports
- Rework: one paid report with strong usefulness feedback
- Kill or pause: zero payments and no meaningful follow-up interest

## Next build target

Create a small `forge-ai` validation layer before connecting any model to the public FORGE.ONE interface.

The model may propose. Code must verify.
