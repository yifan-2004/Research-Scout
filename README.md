# Research Scout

A research agent with a browser interface for **vision literature reviews** and **product competitor analysis**. Define a topic, collect evidence and export a report with citations.

## Features

- Research web pages, local documents or both, depending on configuration.
- Choose Chinese research templates directly on the home page.
- Compare methods, datasets and metrics, or investigate product capabilities and pricing.
- Review report claims with an [evidence checklist](scout/evidence-review.md).

## Quick start

Python 3.12+. Run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows, activate with `.venv\Scripts\activate` and use `copy .env.example .env`.

Set `OPENAI_API_KEY` and `TAVILY_API_KEY` in `.env`, then start:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open [localhost:8000](http://127.0.0.1:8000), choose a workflow and replace its `{{variables}}`. Selecting a template only fills the question; start research manually. The templates are Chinese; most interface text is English.

Research tasks use configured external model/search services, which may charge for requests and receive questions or document excerpts. [Model configuration](docs/docs/gpt-researcher/gptr/config.md) · [Docker setup](docs/docs/gpt-researcher/getting-started/getting-started-with-docker.md)

## Workflows

| Template | Focus |
|---|---|
| [Vision literature review](scout/vision-literature.md) | Method comparison, dataset splits, metrics and reproduction planning |
| [Product competitor analysis](scout/competitor-diligence.md) | User problems, capabilities, pricing and interview planning |

[Machine-readable templates](frontend/scout-workflows.json)

## Checks

```bash
python3 scout/verify.py
python3 scout/audit_snapshot.py
```

Offline checks cover templates, interface wiring and licensing files. Full research execution and Docker builds have not been validated here; report claims still need review.

## License

[Apache-2.0](LICENSE) · [Source](https://github.com/assafelovic/gpt-researcher) · [Licensing notes](docs/PROVENANCE.md)
