# NRR-Transfer: Cross-Domain Transfer of Phase 1.5 Operators Under Fixed Interface Constraints

NRR-Transfer is a cross-domain package for testing **ambiguity-preserving inference** outside a single benchmark domain. It evaluates when to avoid **premature commitment in LLM decoding**, how to reduce **semantic collapse** across scenarios, and how to apply a practical **defer vs commit** policy under fixed interface constraints. The repository is intentionally pre-public and minimal: code/schema/scripts for reproducibility are included, while manuscript text and full run outputs are withheld until publication timing allows. The goal is measurable transfer behavior across models and temperatures without inflating claims or hiding boundary conditions. The emphasis is controlled comparison and transparent limits, so users can distinguish transportable behavior from setup-specific effects.

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

- This repository is a reproducibility package (code/schema/scripts).
- Manuscript text files (`.tex`, `.pdf`) are intentionally not included in this pre-arXiv snapshot.
- Full run outputs and generated final figure PNGs are intentionally not included before arXiv posting.

## Current protocol shape

- Protocol: 18 scenarios x 3 models x 2 temperatures x 3 trials
- Re-run script: `experiments/run_universal_3trial.py`
- Scenario schema: `data/universal_scenarios.json`

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
|       `-- README.md              # output policy (pre-submission)
|-- experiments/
|   `-- run_universal_3trial.py
|-- figures/
|   |-- generate_figures_from_results.py
|   `-- README.md                  # output policy (pre-submission)
`-- archive/
    `-- legacy_pre_v28_2026-02-26/   # previous scripts/data kept for traceability
```

## Legacy handling

Pre-v28 transfer scripts are preserved in `archive/legacy_pre_v28_2026-02-26/`.
Legacy full-result datasets are not included in this pre-submission snapshot.

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
