# NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators Under Fixed Interface Constraints

Reference implementation and manuscript package for:

Saito, K. (2026).
"NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators Under Fixed Interface Constraints"
(arXiv submission pending)

Part of the Non-Resolution Reasoning (NRR) research program.
Program Map (series hub): https://github.com/kei-saito-research/nrr-core/blob/main/PROGRAM_MAP.md

NRR is not an anti-LLM framework.
NRR does not replace standard LLM use.
NRR optimizes when to commit and when to defer, under explicit conditions.

## Versioning Note

- Local manuscript versions (for example `v28`) and arXiv versions (`v1`, `v2`, ...) are different numbering systems.
- They do not map 1:1.
- This repository snapshot tracks the local manuscript `v28`.

## Current Snapshot (v28-aligned)

- Protocol: 18 scenarios x 3 models x 2 temperatures x 3 trials
- Total runs: 324
- Total turns: 1,512
- Extraction success: 100% (1512/1512)
- Scenario-model mean tokens/turn:
  - T=0.0: 65.7205
  - T=0.3: 65.7277
  - Mean delta (0.3 - 0.0): 0.0072
  - Max absolute delta: 0.4444

## Repository Structure

```
nrr-transfer/
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- reproducibility.md
|-- manuscript/
|   |-- paper5-nrr-transfer-v28.tex
|   |-- paper5-nrr-transfer-v28.pdf
|   |-- paper5_fig1_horizontal_v2.png
|   |-- paper5_fig2_all_domains.png
|   |-- paper5_fig3_structural_similarity.png
|   |-- paper5_fig4_operator_heatmap.png
|   |-- figures/                     # mirrored manuscript figure assets
|   `-- archive/                     # reserved for older manuscript drafts
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

## Legacy Handling

To avoid losing history, pre-v28 transfer scripts and datasets are not deleted.
They are moved to `archive/legacy_pre_v28_2026-02-26/` and are not used as claim-source artifacts for manuscript v28.

## Reproducibility

See `reproducibility.md` for:
- fixed settings
- run commands
- artifact mapping from data to manuscript figures/claims

## Related Repositories

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
