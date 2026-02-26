# NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators Under Fixed Interface Constraints

Reference implementation package (code/data) for the NRR-Transfer study.

Part of the Non-Resolution Reasoning (NRR) research program.
Program Map (series hub): https://github.com/kei-saito-research/nrr-core/blob/main/PROGRAM_MAP.md

NRR is not an anti-LLM framework.
NRR does not replace standard LLM use.
NRR optimizes when to commit and when to defer, under explicit conditions.

## Publication handling

- This repository is a reproducibility package (code/data/figures).
- Manuscript text files (`.tex`, `.pdf`) are intentionally not included in this pre-arXiv snapshot.

## Current protocol snapshot

- Protocol: 18 scenarios x 3 models x 2 temperatures x 3 trials
- Total runs: 324
- Total turns: 1,512
- Extraction success: 100% (1512/1512)
- Scenario-model mean tokens/turn:
  - T=0.0: 65.7205
  - T=0.3: 65.7277
  - Mean delta (0.3 - 0.0): 0.0072
  - Max absolute delta: 0.4444

## Repository structure

```
nrr-transfer/
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- reproducibility.md
|-- data/
|   |-- universal_scenarios.json
|   `-- results/
|       `-- universal_3trial_results.json
|-- experiments/
|   `-- run_universal_3trial.py
|-- figures/
|   |-- generate_figures_from_results.py
|   |-- paper5_fig2_all_domains.png
|   `-- paper5_fig4_operator_heatmap.png
`-- archive/
    `-- legacy_pre_v28_2026-02-26/   # previous scripts/data kept for traceability
```

## Legacy handling

Pre-v28 transfer scripts and datasets are preserved in `archive/legacy_pre_v28_2026-02-26/`.
They are retained for traceability and are not claim-source artifacts for the current snapshot.

## Reproducibility

See `reproducibility.md` for fixed settings, run commands, and artifact mapping.

## Related repositories

- https://github.com/kei-saito-research/nrr-core
- https://github.com/kei-saito-research/nrr-phi
- https://github.com/kei-saito-research/nrr-ime

## License

CC BY 4.0. See `LICENSE`.

## Contact

Kei Saito
Independent Researcher, Japan
ORCID: https://orcid.org/0009-0006-4715-9176
Email: kei.saito.research@gmail.com
