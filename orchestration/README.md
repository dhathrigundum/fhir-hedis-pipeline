# Local Airflow (Docker Compose)

Runs Airflow locally for development — no cloud account needed. See
`docker-compose.yaml` (Airflow's official reference compose file) and
`dags/hedis_pipeline_dag.py` (placeholder DAG skeleton).

## Start

```bash
docker compose up -d
```

Then open http://localhost:8080.

## Pause (keeps containers + data, fastest to resume)

```bash
docker compose stop
```

Resume with:

```bash
docker compose start
```

## Full teardown (keeps images + data volumes — no re-pull needed next time)

```bash
docker compose down
```

## Full reset (wipes Airflow's metadata DB — DAG history, connections, etc.)

```bash
docker compose down -v
```

**Avoid `docker system prune` / `docker rmi` on the Airflow/Postgres/Redis
images** unless done with the project for good — they're ~1-2GB combined,
and this environment has hit repeated network failures re-pulling them.

**Habit:** `docker compose stop` when done for the session, `docker compose
start` to pick back up.