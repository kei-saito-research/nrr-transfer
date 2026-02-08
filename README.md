# NRR-Universal: Universal Generality Across Six Domains

Reference implementation for the paper:

**"NRR-Universal: Universal Generality Across Six Domains"**  
Kei Saito (2026)  
*Manuscript in preparation* (arXiv submission pending)

Part of the Non-Resolution Reasoning (NRR) research program.

---

## Overview

This repository contains the experimental validation code for NRR Phase 1.5 universality, demonstrating:

- **100% extraction success** across 18 scenarios spanning 6 domains
- **Operator selection variation**: 0%-100% demonstrating true generality
- **Consistent token efficiency**: 67.6-85.3 tokens/turn across all domains
- **No domain-specific tuning** required

---

## Repository Structure

```
nrr-universal/
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

Output:
```
Total scenarios: 18
Total turns: 84
Extraction success: 84/84 (100%)
Operator distribution: 69σ (82.1%), 15δ (17.9%)
Overall efficiency: 75.8 tokens/turn
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

- 18 scenarios across 6 domains
- Turn-by-turn operator extraction
- Token consumption statistics
- Operator selection patterns

---

## Key Results

### Domain Coverage

| Domain | Scenarios | Turns | Tokens | Avg/Turn |
|--------|-----------|-------|--------|----------|
| IME | 3 | 27 | 2302 | 85.3 |
| RAG | 2 | 10 | 779 | 77.9 |
| Agent | 1 | 6 | 437 | 72.8 |
| Planning | 4 | 13 | 916 | 70.5 |
| Multi-agent | 4 | 14 | 947 | 67.6 |
| Multimodal | 4 | 14 | 983 | 70.2 |
| **Total** | **18** | **84** | **6364** | **75.8** |

### Operator Selection Patterns

- **100% σ (strengthen)**: 9 scenarios (IME, RAG, Agent, some Planning)
- **Mixed σ/δ**: 5 scenarios (some Planning, Multimodal)
- **100% δ (dampen)**: 2 scenarios (Planning)
- **Range**: 0%-100%, demonstrating true architectural generality

### Extraction Success

- **84/84 turns (100%)**: Successful operator extraction
- **No domain-specific tuning**: Pure Phase 1.5 architecture
- **Consistent efficiency**: 67.6-85.3 tokens/turn despite operator variation

---

## Citation

If you use this code, please cite:

```bibtex
@article{saito2026universal,
  title={NRR-Universal: Universal Generality Across Six Domains},
  author={Saito, Kei},
  journal={arXiv preprint},
  year={2026},
  note={Manuscript in preparation}
}
```

---

## Related Repositories

- [NRR-Core](https://github.com/kei-saito-research/nrr-core)
- [NRR-Phi](https://github.com/kei-saito-research/nrr-phi) - Text-to-state mapping
- [NRR-IME](https://github.com/kei-saito-research/nrr-ime) - Structure-aware optimization

---

## Commercial Use

This work is released openly under a CC BY 4.0 license.

If you plan to use it in a commercial or production setting,
a short message would be appreciated.
It helps me understand real-world use and continue the research.

## License

CC BY 4.0 License. See [LICENSE](LICENSE).

---

## Contact

Kei Saito  
Independent Researcher, Japan  
ORCID: [0009-0006-4715-9176](https://orcid.org/0009-0006-4715-9176)  
Email: kei.saito.research@gmail.com
