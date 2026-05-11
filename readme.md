# SNCF Disruptions Pipeline

A production-grade data pipeline built with **Dagster** that ingests, cleans, and stores real-time disruption data from the [SNCF Open Data API](https://data.sncf.com). Designed with modularity and observability in mind, this project showcases modern data engineering practices using a fully local, open-source stack.

---

## Overview

The pipeline fetches live disruption events from the SNCF network, normalizes the raw JSON responses into structured DataFrames, applies data quality checks, and persists clean records to Parquet for downstream consumption. All orchestration is handled by Dagster, providing full lineage tracking, metadata logging, and a local web UI out of the box.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | [Dagster](https://dagster.io/) 1.13+ |
| Data Processing | [Polars](https://pola.rs/) 1.40+ |
| Transformations | [dbt-DuckDB](https://github.com/duckdb/dbt-duckdb) |
| HTTP Client | Requests |
| Runtime | Python 3.12 |
| Package Manager | [uv](https://github.com/astral-sh/uv) |

---

## Architecture

```
SNCF Open API
      │
      ▼
┌─────────────────────┐
│  SNCFResource       │  ← Dagster ConfigurableResource
│  (HTTP + Auth)      │     handles auth & retries
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   Ingestion         │  ←  Ingest raw data
│                     │     JSON → Polars DataFrame
│                     │     + metadata preview in UI
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Transformation     │  ← Transform raw data
│                     │     column selection, null drops
│                     │     using dbt
└─────────────────────┘
```

---

## Project Structure

```
sncf-pipeline/
├── dagster_pipeline/
│   ├── assets/
│   │   ├── __init__.py
│   │   └── ingestion.py       # Asset definitions
|   ├── __init__.py   
│   ├── config.py              # Environment variable loading
│   ├── definitions.py         # Dagster Definitions entry point
│   ├── resources.py           # SNCFResource (ConfigurableResource)
│   └── schedules.py           # (Scheduled runs)
├── dashboard/
    └── dashboard_app.py       # Dashboard to display insights
├── data/                      # Local duckdb DB
├── dbt-scnf/
│   ├── models/
│   │   ├── marts/ 
│   │   └── staging/
│   ├── dbt_project.yml        # Config file for dbt
│   ├── dev.duckdb
│   └── profiles.yml           # Dbt resources for database usage
├── pyproject.toml
└── uv.lock
```

---

## Key Features

- **Software-defined assets** — each transformation step is an explicit, testable Dagster asset with upstream dependencies declared via `deps`.
- **Configurable resource injection** — the `SNCFResource` wraps the API client and is injected at runtime, making it easy to swap for a mock in tests.
- **Metadata-enriched runs** — row counts and DataFrame previews (rendered as Markdown tables) are attached to each asset materialization and visible in the Dagster UI.
- **Polars for performance** — columnar processing with `pl.json_normalize` and lazy evaluation keeps memory usage low even on large payloads.
- **dbt-DuckDB integration** — the dependency stack includes `dbt-duckdb` for SQL-based transformation layers on top of the ingested data.

---

## Getting Started

### Prerequisites

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) package manager
- A valid SNCF API token ([register here](https://numerique.sncf.com/startup/api/))

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/sncf-pipeline.git
cd sncf-pipeline

# Install dependencies
uv sync
```

### Configuration

Create a `.env` file at the project root:

```env
SNCF_TOKEN=your_api_token_here
```

### Running the Pipeline

```bash
# Launch the Dagster web UI
uv run dagster dev

# Navigate to http://localhost:3000
# Materialize assets from the Asset Catalog
```

---

## Data Flow

1. **Ingestion** — Calls the SNCF `/disruptions` endpoint with a configurable `count` parameter, deserializes the JSON payload, and normalizes nested fields into a flat Polars DataFrame.

2. **Transform** — TO DO using dbt

---

## Roadmap

- [ ] Implement dbt models on top for data transformation
- [ ] Implement dashboard for presentation of data insights (in a perfect world I would use polars but Im too bad actually)
- [ ] Implement logic to get historical data (since it passes through 3 status values)
- [ ] Add asset checks for data quality validation
- [ ] Containerize with Docker for deployment
- [ ] Integrate with a cloud storage backend (S3 / GCS)

---

## License

MIT