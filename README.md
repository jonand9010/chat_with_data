# chat_with_data

This repository contains an MVP skeleton for an AI Reliability Analyst focused on NASA C-MAPSS turbofan degradation analysis.

## Project structure

- data/ for raw, interim, and processed datasets
- src/reliability_analyst/ for the Python package
- configs/ for semantic layer definitions
- tests/ for regression and unit tests

## Quick start

1. Install uv if needed: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
2. Create and sync the environment with `uv sync --group dev`.
3. Run tests with `uv run pytest`.
4. Add data files under data/raw/ to start building the pipeline.

## Current scaffold

- package layout for data, semantic, analytics, agent, plotting, and app layers
- starter analytics tools for summarizing an engine and ranking degrading engines
- semantic layer configuration and a basic planner schema