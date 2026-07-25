# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this project is
A healthcare ELT/HEDIS portfolio project. Full problem statement is in
`README.md`. Full scope reasoning and phase checklist is in `PLANNING.md`.

## Before doing any work in a new session
1. Read `README.md` for the problem statement and architecture overview.
2. Read `PLANNING.md` — check the "Phases" checklist for current status
   and the "Open Decisions" section for anything unresolved.
3. Read `docs/decisions.md` before making or suggesting any architecture,
   tool, or scope tradeoff. Don't re-litigate a decision already logged
   there without flagging that you're doing so and why.
4. Read `docs/data_generation.md` for the exact dataset generation
   parameters already in use — do not regenerate or suggest regenerating
   the population without an explicit reason, since patient IDs are reused
   across every phase of this project.
5. If `docs/data_dictionary.md` or `docs/measure_spec_cbp.md` exist, read
   them before touching ingestion, dbt models, or measure logic.

## Ground rules for this project
- **ELT, not ETL.** Land raw data as close to source shape as possible;
  do transformation in-warehouse via dbt, not in the ingestion scripts.
- **Every real tradeoff gets logged** in `docs/decisions.md` in its
  existing format (decision, options considered, why, date) — including
  ones you make or recommend during a session.
- **Scope discipline.** Streaming, Hybrid HEDIS methodology, multi-cloud,
  and Cloud Composer are explicitly out of scope per `docs/decisions.md`.
  Don't reintroduce them without flagging that this contradicts a logged
  decision.
- **Financial/contract data is synthetic and must stay labeled as such**
  anywhere it appears (code comments, dbt model descriptions, dashboard
  labels) — never presented as if derived from real payer data.
- **Never read, print, cat, copy, or move any credentials or key file**
  (GCP service account keys, `.env` contents, API keys). Reference cloud
  credentials only via the `GOOGLE_APPLICATION_CREDENTIALS` environment
  variable or an already-authenticated `gcloud` session — both set up
  outside this session, not something to inspect or debug by viewing the
  file's contents. If a connection fails, debug via error messages and
  `gcloud auth list` / `gcloud config list`, not by opening the key file.
- Keep `PLANNING.md`'s "Log" section updated with a dated entry summarizing
  what changed, at the end of any session that ships real progress.

## Current phase
Check `PLANNING.md` → "Phases" checklist for the authoritative current
state; do not assume based on this file alone, as it is not updated per
session.

## Repo structure
```
├── README.md
├── PLANNING.md
├── raw_data_sample/     # small committed sample; full raw data git-ignored
├── ingestion/           # Python load scripts (raw -> warehouse)
├── dbt/                 # dbt project
├── orchestration/       # Airflow DAGs (run locally via Docker)
├── dashboards/          # BI files / exported screenshots
└── docs/                # decisions.md, data_generation.md, specs, dictionary
```
