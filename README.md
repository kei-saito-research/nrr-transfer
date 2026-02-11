# NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators

Reference implementation for the paper:

**"NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators"**  
Kei Saito (2026)  
*Manuscript in preparation* (arXiv submission pending)

Part of the Non-Resolution Reasoning (NRR) research program.
Program Map (series hub): [NRR Program Map](https://github.com/kei-saito-research/nrr-core/blob/main/PROGRAM_MAP.md)

---

## Overview

This repository contains the experimental validation code for NRR Phase 1.5 transferability, demonstrating:

- **Cross-domain protocol**: 324 runs and 1,512 turns (18 scenarios x 3 models x 2 temperatures x 3 trials)
- **100% extraction success** across all runs (1,512/1,512 turns)
- **Temperature-robust efficiency**: mean difference 0.0072 tokens/turn (T=0.3 vs T=0.0), max absolute difference 0.4444
- **Operator-pattern generality**: 0%-100% delta usage by scenario while preserving 100% extraction success

---

## Repository Structure

```
nrr-transfer/
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── experiments/
│   ├── cross_domain_validation.py   # 18-scenario validation
│   ├── operator_analysis.py         # Operator selection patterns
│   └── experimental_data.json       # Complete experimental results
└── figures/
    ├── generate_fig1.py             # Operator selection heatmap
    └── generate_fig2.py             # Domain summary charts
```

---

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Experiments

**Cross-Domain Validation (18 scenarios):**
```bash
python experiments/cross_domain_validation.py
```

**Operator Analysis:**
```bash
python experiments/operator_analysis.py
```

Output shows operator selection patterns across all scenarios, demonstrating 0%-100% variation.

### Generate Figures

```bash
python figures/generate_fig1.py  # Operator selection heatmap
python figures/generate_fig2.py  # Domain summary charts
```

Figures will be saved in the `figures/` directory.

---

## Experimental Data

All experimental results are stored in `experiments/experimental_data.json`:

- Full protocol logs for 324 runs (18 scenarios x 3 models x 2 temperatures x 3 trials)
- Turn-by-turn operator extraction (1,512 turns total)
- Token consumption statistics and temperature robustness metrics
- Operator selection patterns by domain and scenario

---

## Key Results (Paper-Aligned)

- **Total runs**: 324
- **Total turns**: 1,512
- **Extraction success**: 100% (1,512/1,512)
- **Overall efficiency**:
  - T=0.0: 65.720 tokens/turn (scenario-model mean)
  - T=0.3: 65.728 tokens/turn (scenario-model mean)
  - Mean delta (0.3 - 0.0): 0.0072 tokens/turn
  - Max absolute temperature difference: 0.4444

### Per-Domain Token Usage (T=0.3, averaged across models)

| Domain | Avg tokens/turn |
|--------|------------------|
| IME | 76.5 |
| RAG | 69.6 |
| Agent | 64.1 |
| Planning | 63.6 |
| Multi-agent | 61.0 |
| Multimodal | 63.0 |
| **Overall (18 scenarios)** | **65.7** |

### Operator Selection (all 324 runs)

- Objective-leaning domains (IME, RAG, Agent): 686 sigma (88.6%), 88 delta (11.4%)
- Subjective-heavy domains (Planning, Multi-agent, Multimodal): 189 sigma (25.6%), 549 delta (74.4%)
- Overall: 875 sigma (57.9%), 637 delta (42.1%)
- Scenario-level usage spans 0%-100% delta while maintaining 100% extraction success

---

## Citation

If you use this code, please cite:

```bibtex
@article{saito2026universal,
  title={NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators},
  author={Saito, Kei},
  journal={arXiv preprint},
  year={2026},
  note={Manuscript in preparation}
}
```

---

## Related Repositories

- [NRR-Core](https://github.com/kei-saito-research/nrr-core) - Foundational framework
- [NRR-Phi](https://github.com/kei-saito-research/nrr-phi) - Text-to-state mapping
- [NRR-IME](https://github.com/kei-saito-research/nrr-ime) - Structure-aware optimization

---

## Reproducibility

See [`reproducibility.md`](./reproducibility.md) for environment, fixed settings, runnable commands, and artifact mapping.

---

## Commercial Use

If you plan to use this in a commercial or production setting,
a short message would be appreciated.

## License

CC BY 4.0 License. See [LICENSE](LICENSE).

---

## Reproduction & Issue Reports

If you reproduce results, find discrepancies, or hit bugs, please open an issue:
- https://github.com/kei-saito-research/nrr-transfer/issues

Please include:
- environment (OS, Python version)
- command you ran
- commit hash (if applicable)
- observed output/error logs

---

## Contact

Kei Saito  
Independent Researcher, Japan  
ORCID: [0009-0006-4715-9176](https://orcid.org/0009-0006-4715-9176)  
Email: kei.saito.research@gmail.com
