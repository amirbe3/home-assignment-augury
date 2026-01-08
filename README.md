# Home Assignment – Validation/Automation Engineer

This repo is a small in-memory simulation of a simple IoT system (Node + Endpoints),
with a few update rules (OTA/DFU) and Robot Framework tests around it.

I focused on:
- keeping the code easy to follow
- writing tests that reflect the requirements and edge cases

## Project structure

- `src/`
  - `models.py`      : Node / Endpoint data models + OTA/DFU update rules
  - `augury_api.py`  : in-memory “API” helpers (no real network)
  - `demo.py`        : small manual demo (OTA happy flow example)
- `tests/`           : Robot Framework tests
- `docs/`            : signal processing answers (document)

## How to run

### 1) Install dependencies
```bash
pip install -r requirements.txt

