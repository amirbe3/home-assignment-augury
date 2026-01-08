# Home Assignment – Validation / Automation Engineer

This repository contains a small in-memory simulation of a simple IoT system
(Node + Endpoints), with basic OTA / DFU update rules and Robot Framework tests.

The goal of the assignment was to demonstrate reasoning, testing approach,
and the ability to validate expected behavior and edge cases.

I focused on:
- keeping the code easy to follow and readable
- writing tests that reflect the requirements and failure scenarios

## Project structure

- `src/`
  - `models.py`      : Node / Endpoint data models + OTA / DFU update rules
  - `augury_api.py`  : in-memory API helpers (no real network calls)
  - `demo.py`        : small manual demo showing a successful OTA flow
- `tests/`
  - Robot Framework tests for DFU and OTA scenarios
- `docs/`
  - signal processing answers (document)

## How to run

### 1) Install dependencies
```bash
pip install -r requirements.txt
