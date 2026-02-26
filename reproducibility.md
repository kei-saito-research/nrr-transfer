# Reproducibility (NRR-Transfer code/data snapshot)

## Scope

This repository snapshot provides reproducibility assets (code/data/figures).
Manuscript text files (`.tex`, `.pdf`) are intentionally excluded in this pre-arXiv state.

Claim-source dataset:
- `data/results/universal_3trial_results.json`

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

python3 experiments/run_universal_3trial.py \
  --scenarios-json data/universal_scenarios.json \
  --out data/results/universal_3trial_results.json \
  --trials 3 \
  --temperatures 0.3,0.0 \
  --models claude,gpt,gemini \
  --max-tokens 200 \
  --alpha 0.4
```

### B) Regenerate figures from finalized results

```bash
python3 figures/generate_figures_from_results.py
```

Outputs:
- `figures/paper5_fig2_all_domains.png`
- `figures/paper5_fig4_operator_heatmap.png`

## Artifact map

- Scenario definitions:
  - `data/universal_scenarios.json`
- Raw/aggregated run output:
  - `data/results/universal_3trial_results.json`
- Figure generation script:
  - `figures/generate_figures_from_results.py`
- Generated Figure 2:
  - `figures/paper5_fig2_all_domains.png`
- Generated Figure 4:
  - `figures/paper5_fig4_operator_heatmap.png`

## Known notes

- PNG files may differ bit-for-bit across environments while remaining visually equivalent.
- API-based reruns can produce small token-count variation due to provider-side changes over time.
- The included `data/results/universal_3trial_results.json` is the claim-source snapshot for this repository state.
