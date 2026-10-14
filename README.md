# BaanDee Living Class 1 Student Package

This package accompanies the instructor-led demonstration of the **Delayed Order Support Copilot**. BaanDee Living, its customers, orders and operational records are fictional. All data are synthetic.

Class 1 is a demonstration rather than a coding lab. You may use this package after class to inspect the data, rerun the notebook and explore how the components connect.

## What the project demonstrates

- inspecting and cleaning exported CSV data with pandas;
- joining tickets, customers, orders, order lines, products and inventory;
- handling inconsistent identifiers through documented rules;
- quarantining ambiguous records instead of silently changing them;
- retrieving current operational evidence through a local FastAPI service;
- applying an explicit service policy before generating language;
- connecting Python functions to a Gradio interface; and
- protecting important behavior with tests.

## macOS setup

Use Python 3.11 or 3.12. Open Terminal, move into the extracted folder and run:

```bash
chmod +x scripts/*.sh
./scripts/setup_mac.sh
./scripts/smoke_test_mac.sh
```

Internet access is required during the first setup to install packages. The smoke test should end with:

```text
MAC_SMOKE_TEST_PASS
```

## Start the project

Open two Terminal windows.

Terminal 1:

```bash
cd /path/to/BaanDee_Class1_Student
./scripts/start_api.sh
```

Terminal 2:

```bash
cd /path/to/BaanDee_Class1_Student
./scripts/start_app.sh
```

The API documentation is available at `http://127.0.0.1:8000/docs`. The Gradio application normally opens at `http://127.0.0.1:7860`.

To explore the notebook, use a third Terminal:

```bash
cd /path/to/BaanDee_Class1_Student
./scripts/start_notebook.sh
```

Press `Control+C` in each Terminal to stop a running service.

## Demonstration records

| Ticket | Main data behavior |
|---|---|
| `TKT-260731-042` | Short order reference, approved crosswalk and stale export versus current API |
| `TKT-260731-099` | Unverified order that requires human follow-up |
| `TKT-260731-117` | Export/API freshness conflict with an API-supplied delivery estimate |

## Project map

```text
BaanDee_Class1_Student/
  data/raw/             original synthetic exports
  data/checkpoints/     cleaned and joined checkpoints
  data/ground_truth/    fixed mappings and demonstration fixtures
  notebooks/            annotated Class 1 notebook
  api/                  local FastAPI service and JSON fixtures
  src/                  shared cleaning, evidence, policy and app logic
  tests/                repeatable behavior checks
  scripts/              setup, start, reset and smoke-test commands
  docs/student/         company brief, observation sheet and project preview
```

## AI mode and API keys

The default `fixture` mode is synthetic and does not require an AI API key. It demonstrates the application path without claiming live-model quality.

If you later use a live model, keep the key in your own environment. Never write a real key into the notebook, source code, screenshots, submitted work or Git repository. The included `.env.example` contains placeholders only.

## Using Git for your own work

Do not commit `.venv`, `.env`, logs, executed notebooks, caches or API keys. The included `.gitignore` excludes these local files.

For the final project, your team should create its own repository and record meaningful changes with clear commit messages. The complete final-project brief and assessment requirements will be provided separately.

## Student documents

- `docs/student/COMPANY_BRIEF.md`
- `docs/student/OBSERVATION_SHEET.md`
- `docs/student/FINAL_PROJECT_PREVIEW.md`

