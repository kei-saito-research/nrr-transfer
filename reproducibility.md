# Reproducibility (NRR-Transfer)

## Scope

This repository provides manuscript and reproducibility assets (code/schema/scripts).
The primary 324-run log is included at `data/results/transfer_3trial_results.json`.

Legacy pre-v28 materials:
- `archive/legacy_pre_v28_2026-02-26/`

## Environment

- Python: 3.10+
- Libraries: `requirements.txt`
  - anthropic
  - openai
  - google-generativeai
  - matplotlib
  - numpy

## Fixed protocol settings

- Models: Claude Sonnet 4, GPT-4o-mini, Gemini 2.0 Flash
- Temperatures: 0.3 (main), 0.0 (robustness)
- Trials: 3 per condition
- Scenarios: 18 (6 domains)
- Total: 324 runs, 1,512 turns
- State update alpha: 0.4
- Max output tokens: 200

## Run commands

### A) Re-run protocol (requires API keys)

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."
export GEMINI_API_KEY="..."   # or GOOGLE_API_KEY

python3 experiments/run_transfer_3trial.py \
  --scenarios-json data/transfer_scenarios.json \
  --out /path/to/private_outputs/transfer_3trial_results.json \
  --trials 3 \
  --temperatures 0.3,0.0 \
  --models claude,gpt,gemini \
  --max-tokens 200 \
  --alpha 0.4
```

### B) Regenerate figures from included results

```bash
python3 figures/generate_figures_from_results.py
```

Outputs:
- `figures/paper5_fig2_all_domains.png`
- `figures/paper5_fig4_operator_heatmap.png`

Note: generated PNGs can vary slightly across environments while preserving the same aggregate trends.

## Artifact map

- Scenario definitions:
  - `data/transfer_scenarios.json`
- Figure generation script:
  - `figures/generate_figures_from_results.py`
- Primary run log:
  - `data/results/transfer_3trial_results.json`
- Result checksum:
  - `data/results/checksums_sha256.txt`
- Output policy notes:
  - `data/results/README.md`
  - `figures/README.md`

## Known notes

- PNG files may differ bit-for-bit across environments while remaining visually equivalent.
- API-based reruns can produce small token-count variation due to provider-side changes over time.
