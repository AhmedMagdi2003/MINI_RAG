# MINI_RAG

An API service for ingesting documents, indexing their content, and answering natural-language questions through retrieval-augmented generation (RAG). The current application code exposes separate data and NLP routes and constructs its language-model, vector-store, and relational-database integrations through provider/configuration modules.

> **Configuration note:** The repository's older README describes MongoDB/Motor. The inspected application startup instead initializes PostgreSQL through SQLAlchemy, and the vector-store factory supports local Qdrant. The checked-in Docker Compose file includes MongoDB and pgvector/PostgreSQL services, while the current application defaults point to PostgreSQL and local Qdrant. Confirm the intended service setup before treating that Compose file as a complete deployment recipe.

## Capabilities

- Upload and process documents through the data routes.
- Index document content and search it through the NLP routes.
- Submit questions for retrieval-grounded answers.
- Configure generation and embedding providers through environment settings.
- Persist relational application data with PostgreSQL and use the configured vector store for retrieval.

These are API capabilities; the repository does not establish a production-hosted UI or deployment.

## Architecture

```text
Client
  ├── data routes: upload and process documents
  └── NLP routes: index, search, and answer
          ├── language-model provider factory
          ├── vector-store provider factory (Qdrant implementation)
          └── PostgreSQL access through SQLAlchemy
```

The routes and provider factories are under `src/`. The current vector database factory supports Qdrant with a local persistence path. Available model providers and environment names should be taken from `src/.env.example` and the corresponding provider modules.

## Requirements

- Python version compatible with the pinned dependencies in `requirements.txt`.
- A PostgreSQL instance reachable using the database settings expected by the application.
- Provider credentials/configuration for the selected model and embedding services, if using hosted providers.
- Local Qdrant persistence configured for the current vector-store implementation.

## Local setup

From the repository root:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `src/.env.example` to the environment file location loaded by the application, then set database connection values and the desired provider configuration. The example file is under `src/`; there is no root-level `.env.example` in the inspected tree. Do not commit secrets.

Prepare PostgreSQL and apply the repository's supported migrations before starting the API. Exact database initialization and Compose alignment should be confirmed against the current migration/configuration state; the checked-in Compose services do not directly match the application's local-Qdrant default.

Start the API from the repository root:

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000/docs` to inspect the routes and request schemas exposed by the running app.

## API usage

Use the generated OpenAPI page to review the exact endpoints and payload schemas. The route groups cover document upload/processing and NLP indexing, search, and question answering. Provide documents using the upload schema, index processed content, then query the indexed material. Request and response field details should be treated as defined by the current route models rather than inferred from this summary.

## Configuration and operational notes

- Default generation and embedding settings are examples, not production credentials or service guarantees.
- The checked-in Compose file currently starts MongoDB and PostgreSQL/pgvector, but inspected startup code uses PostgreSQL and a local Qdrant store; confirm intended service wiring before relying on Compose.
- Review provider implementations and model limits before selecting a deployment configuration.
- No authentication, access-control, or production-hardening claims are made here.

## Project objective

Provide a modular backend foundation for document-based question answering, with API routes separated from language-model and vector-store provider selection.

## License

See the repository's license file, if present.
