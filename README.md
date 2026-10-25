# MINI_RAG

**Bring your own documents and ask questions grounded in their content.** MINI_RAG is a modular API project that demonstrates a document-to-answer RAG experience, from ingestion and indexing to retrieval-backed question answering.

[View the source](https://github.com/AhmedMagdi2003/MINI_RAG) · [Open the local API docs](http://127.0.0.1:5000/docs) after running the service

## The project

The objective is to provide a small, inspectable foundation for document-based question answering. Data routes handle document operations; NLP routes expose indexing, search, and question-answering capabilities. Model and vector-store integrations are separated behind provider modules so the application can be configured without embedding every choice in the route layer.

## What it demonstrates

- Document upload and processing through the API.
- Indexing and semantic retrieval over document content.
- Natural-language questions answered using retrieved context.
- Configurable language-model and vector-store providers.
- A FastAPI surface with generated OpenAPI documentation.

## How the experience works

Documents enter through the data API and are processed for indexing. A question is sent through the NLP API, which retrieves relevant indexed content and uses the configured language model to form a grounded response. The project is an API backend; the repository does not establish a hosted end-user interface or production deployment.

## Try it locally

Install the dependencies, configure the environment values in src/.env.example, and provide the database and model-provider settings required by the selected configuration. Start the API from the repository root:

~~~bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 5000
~~~

Then open the local API docs at http://127.0.0.1:5000/docs to inspect routes and request schemas. Do not commit credentials or API keys.

## Built with

Python · FastAPI · PostgreSQL/SQLAlchemy · Qdrant provider · LLM and embedding provider modules

## Setup note

The repository contains older documentation and Compose services that describe MongoDB/Motor and PostgreSQL/pgvector, while the inspected current application code initializes PostgreSQL through SQLAlchemy and provides a local Qdrant vector-store implementation. Treat those deployment instructions as needing reconciliation before relying on Compose; verify the service configuration and database initialization against the current code.

## About

Built by Ahmed Magdi as a modular RAG API project. [Repository](https://github.com/AhmedMagdi2003/MINI_RAG)
