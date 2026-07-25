# Data Generation

## Source
[Synthea](https://github.com/synthetichealth/synthea) — synthetic patient
population generator. Self-generated, not a pre-packaged download, so the
population, disease-module mix, and history depth are chosen deliberately
for this project rather than inherited from a generic sample.

## Generation command
```bash
./run_synthea -p <POPULATION_SIZE> <STATE> \
  --exporter.fhir.export=true \
  --exporter.fhir.bulk_data=false \
  --exporter.years_of_history=<YEARS>
```

## Final parameters used
| Parameter | Value | Why |
|---|---|---|
| Population size | 3,000 (target living population; 3,454 total patient records exported, including deceased) | Large enough for a real Controlling High Blood Pressure denominator |
| State module | Massachusetts | |
| Years of history | 5 | Needs to comfortably cover a 12-month HEDIS lookback |
| Synthea version / commit | `7e08387c68a7f0e21d13076609a159fd473fc902` (2026-07-22) | Record for reproducibility |
| Date generated | 2026-07-25 | |

## Resource types confirmed present in output
- [x] Patient
- [x] Condition
- [x] Encounter
- [x] Observation
- [x] Claim
- [x] ExplanationOfBenefit
- [x] Coverage
- [x] MedicationRequest

## Validation notes
Hypertension condition prevalence: 785 of 3,454 patients (~22.7%) —
a solid, non-trivial CBP denominator. Small-batch test run (20 patients)
also confirmed Claim, Coverage, ExplanationOfBenefit, and
MedicationRequest resources present alongside the core clinical
resources. Population treated as final as of 2026-07-25 — patient IDs
from this run are reused across every later phase of the project.

## Reproducing this dataset
Anyone cloning this repo can regenerate the exact same *shape* of data
(patient IDs will differ, Synthea does not seed reproducibly by default)
by running the command above with the parameters in the table.
