# NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators Under Fixed Interface Constraints

NRR-Transfer is a cross-domain package for testing **ambiguity-preserving inference** outside a single benchmark domain. It evaluates when to avoid **premature commitment in LLM decoding**, how to reduce **semantic collapse** across scenarios, and how to apply a practical **defer vs commit** policy under fixed interface constraints. This repository includes manuscript artifacts together with code/schema/scripts for reproducibility. The goal is measurable transfer behavior across models and temperatures without inflating claims or hiding boundary conditions. The emphasis is controlled comparison and transparent limits, so users can distinguish transportable behavior from setup-specific effects.

**Quick links**
- arXiv: pending (pre-submission; no public URL yet)
- [Positioning (NRR vs related approaches)](./docs/positioning.md)
- [Search Keywords and Weekly Rank Log](./docs/keywords.md)

**EN/JA query terms**
- `early commitment` = `早期確定`
- `ambiguity-preserving inference` = `曖昧性保持推論`

Part of the Non-Resolution Reasoning (NRR) research program.
Program Map (series hub): https://github.com/kei-saito-research/nrr-core/blob/main/PROGRAM_MAP.md

NRR is not an anti-LLM framework.
NRR does not replace standard LLM use.
NRR optimizes when to commit and when to defer, under explicit conditions.

## DOI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18793345.svg)](https://doi.org/10.5281/zenodo.18793345)

## Publication handling

- This repository includes manuscript and reproducibility assets.
- Current manuscript snapshot is stored under `manuscript/current/`.
- Primary experiment logs for the 324-run protocol are included at `data/results/transfer_3trial_results.json`.
- Generated final figure PNGs from private reruns are not committed by default.

## Current protocol shape

- Protocol: 18 scenarios x 3 models x 2 temperatures x 3 trials
- Re-run script: `experiments/run_transfer_3trial.py`
- Scenario schema: `data/transfer_scenarios.json`

## Repository structure

```
nrr-transfer/
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- reproducibility.md
|-- manuscript/
|   `-- current/
|       |-- paper5-nrr-transfer-v30.tex
|       |-- paper5-nrr-transfer-v30.pdf
|       |-- paper5_fig1_horizontal_v2.png
|       |-- paper5_fig2_all_domains.png
|       |-- paper5_fig3_structural_similarity.png
|       |-- paper5_fig4_operator_heatmap.png
|       `-- checksums_sha256.txt
|-- data/
|   |-- transfer_scenarios.json
|   `-- results/
|       `-- README.md              # output policy (pre-submission)
|-- experiments/
|   `-- run_transfer_3trial.py
|-- figures/
|   |-- generate_figures_from_results.py
|   `-- README.md                  # output policy (pre-submission)
`-- archive/
    `-- legacy_pre_v28_2026-02-26/   # previous scripts/data kept for traceability
```

## Legacy handling

Pre-v28 transfer scripts are preserved in `archive/legacy_pre_v28_2026-02-26/`.
Legacy full-result datasets are not bundled in `archive/`; the canonical run log is `data/results/transfer_3trial_results.json`.

## Reproducibility

See `reproducibility.md` for fixed settings, run commands, and artifact mapping.

## Related repositories

- https://github.com/kei-saito-research/nrr-core
- https://github.com/kei-saito-research/nrr-phi
- https://github.com/kei-saito-research/nrr-ime

## License

CC BY 4.0. See `LICENSE`.

## Collaboration Style

I support written technical Q&A, concept clarification, and small evaluation design.

Typical flow:
1. you send questions and context,
2. I return a structured technical response,
3. if needed, I provide an English-ready version for external sharing.

Scope: research interpretation and evaluation planning.  
Out of scope: production integration, implementation outsourcing, ongoing operations, and SLA/deadline commitments.

## Contact

Kei Saito
Independent Researcher, Japan
ORCID: https://orcid.org/0009-0006-4715-9176
Email: kei.saito.research@gmail.com
