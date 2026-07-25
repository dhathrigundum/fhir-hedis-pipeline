# Healthcare Quality & Claims ELT Pipeline

## Status
🚧 Just started. Problem statement and planned approach below; build in
progress. Detailed planning docs and architecture decisions will be added
as the project develops.

## Problem
A regional Medicare Advantage plan's quality team needs to find members
with open HEDIS care gaps (starting with Controlling High Blood Pressure)
before their NCQA submission deadline — using claims, EHR, and pharmacy
data that currently live in silos — with a pipeline a compliance reviewer
could trace end to end.

## Planned approach
A self-generated synthetic patient population (via
[Synthea](https://github.com/synthetichealth/synthea), not a pre-packaged
download) landed raw in cloud storage, loaded into BigQuery, transformed
with dbt (ELT, not ETL), orchestrated with Airflow, and visualized in
Looker Studio — built around one real NCQA HEDIS measure rather than an
invented risk score.

## Why this project
Built to demonstrate ELT, dbt-based transformation, real HEDIS measure
logic, and orchestration — scoped from patterns pulled from actual
healthcare data analyst / data engineer job postings, not guesswork.

## Progress
Follow along here as it's built — this section and the repo structure will
fill in over time.
