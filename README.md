# NRR-IME: Structure-Aware Optimization for Stateful Reasoning on Stateless LLM APIs

Reference implementation for the paper:

**"NRR-IME: Structure-Aware Optimization for Stateful Reasoning on Stateless LLM APIs"**  
Kei Saito (2026)  
*Manuscript in preparation* (arXiv submission pending)

Part of the Non-Resolution Reasoning (NRR) research program.

---

## Overview

This repository contains the experimental validation code for NRR-IME (Interpretation Management Engine), demonstrating:

- **66.2% token reduction** through structure-aware optimization (Phase 1.5)
- **93.3% reduction** with zero-LLM explicit input (Phase 3.0)
- **Consistent efficiency** across diverse IME scenarios (Bank, Spring, Court)

---

## Repository Structure

```
nrr-ime/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── experiments/
│   ├── phase_comparison.py      # Phase 1.0 vs 1.5 vs 3.0 comparison
│   ├── scaling_validation.py    # Cross-scenario validation
│   └── experimental_data.json   # Complete experimental results
└── figures/
    ├── generate_fig1.py         # Phase comparison chart
    └── generate_fig2.py         # Scaling validation chart
```

---

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Experiments

**Phase Comparison (Bank scenario):**
```bash
python experiments/phase_comparison.py
```

Output:
```
Phase 1.0 (Naive):              1207 tokens (5 turns)
Phase 1.5 (Operators):           408 tokens (5 turns) [-66.2%]
Phase 3.0 (Zero-LLM Explicit):    81 tokens (5 turns) [-93.3%]
```

**Scaling Validation (3 scenarios):**
```bash
python experiments/scaling_validation.py
```

Output:
```
Bank    (5 turns):   408 tokens (81.6 avg/turn)
Spring (10 turns):   874 tokens (87.4 avg/turn)
Court  (12 turns):  1020 tokens (85.0 avg/turn)

Phase 1.5 maintains consistent efficiency: 81.6-87.4 tokens/turn
```

### Generate Figures

```bash
python figures/generate_fig1.py  # Phase comparison chart
python figures/generate_fig2.py  # Scaling validation chart
```

Figures will be saved in the `figures/` directory.

---

## Experimental Data

All experimental results are stored in `experiments/experimental_data.json`:

- Phase 1.0, 1.5, 3.0 comparisons
- Bank, Spring, Court scenarios
- Turn-by-turn token consumption
- Operator extraction statistics

---

## Key Results

### Token Efficiency

| Phase | Tokens (5 turns) | Reduction |
|-------|-----------------|-----------|
| 1.0 (Naive) | 1207 | baseline |
| 1.5 (Operators) | 408 | **-66.2%** |
| 3.0 (Zero-LLM) | 81 | **-93.3%** |

### Cross-Scenario Consistency

| Scenario | Turns | Total Tokens | Avg/Turn |
|----------|-------|--------------|----------|
| Bank | 5 | 408 | 81.6 |
| Spring | 10 | 874 | 87.4 |
| Court | 12 | 1020 | 85.0 |

Phase 1.5 maintains 81.6-87.4 tokens/turn across all scenarios.

---

## Citation

If you use this code, please cite:

```bibtex
@article{saito2026ime,
  title={NRR-IME: Structure-Aware Optimization for Stateful Reasoning on Stateless LLM APIs},
  author={Saito, Kei},
  journal={arXiv preprint},
  year={2026},
  note={Manuscript in preparation}
}
```

---

## Related Repositories

- [NRR-Core](https://github.com/kei-saito-research/nrr-framework) - Foundational framework (Paper 1)
- [NRR-Phi](https://github.com/kei-saito-research/nrr-phi-mapping) - Text-to-state mapping (Paper 2)
- [NRR-Operators](https://github.com/kei-saito-research/nrr-operators) - Operator design principles (Paper 3)
- [NRR-Phase1.5](https://github.com/kei-saito-research/nrr-phase1.5) - Universal generality validation (Paper 5)
- [NRR-Hout](https://github.com/kei-saito-research/nrr-hout) - Output-side entropy measurement (Paper H)

---

## License

This code is licensed under CC BY 4.0.  
© 2026 Kei Saito

---

## Contact

Kei Saito  
Independent Researcher, Japan  
ORCID: [0009-0006-4715-9176](https://orcid.org/0009-0006-4715-9176)  
Email: kei.saito.research@gmail.com
