<h3 align="center">Wharf</h3>
<p align="center">
    A self-hosted PaaS — push a Dockerfile, get a live URL, logs, and a managed database.
    <br />
    <br />
    <a href="#introduction"><strong>Introduction</strong></a> ·
    <a href="#features"><strong>Features</strong></a> ·
    <a href="#tech-stack"><strong>Tech Stack</strong></a> ·
    <a href="#architecture"><strong>Architecture</strong></a> ·
    <a href="#quick-start"><strong>Quick Start</strong></a> ·
    <a href="#roadmap"><strong>Roadmap</strong></a>
</p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-work--in--progress-orange">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="python" src="https://img.shields.io/badge/python-3.12-blue">
</p>

## Introduction

Wharf is a self-hosted deployment platform — a minimal, educational take on Heroku/Railway. Point it at a repository or archive containing a Dockerfile, and it builds the image, runs it in an isolated container, and hands back a working public URL, complete with live logs and an optional managed PostgreSQL add-on with zero manual database setup.

This is a portfolio and learning project, built to go deep on real system design and DevOps practices — container orchestration, reverse proxying, service isolation, and CI/CD — rather than to compete with production PaaS platforms.

> 🚧 **Status:** actively under development. See the [Roadmap](#roadmap) for current progress.

## Features

- **Dockerfile → live app** — upload an archive (or connect a repo) and get a running, publicly reachable container
- **Reverse-proxied URLs** — each deployment gets its own subdomain/path via dynamic routing
- **Live logs** — stream container logs straight to the user
- **Managed Postgres add-on** — provision a database per project, `DATABASE_URL` auto-injected, no manual setup
- **Isolated containers** — per-project networks, resource limits, non-root execution
- **JWT auth with refresh rotation** — wrapped in its own gRPC service as a deliberate microservice experiment

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – backend framework
- [Python](https://www.python.org/) – language
- [PostgreSQL](https://www.postgresql.org/) – relational database
- [Redis](https://redis.io/) – caching, rate limiting & refresh-token rotation
- [Docker](https://www.docker.com/) (via [Docker SDK for Python](https://docker-py.readthedocs.io/)) – image builds & container orchestration
- [Traefik](https://traefik.io/) / [Nginx](https://nginx.org/) – reverse proxy & dynamic routing
- [gRPC](https://grpc.io/) + [Protocol Buffers](https://protobuf.dev/) – auth microservice communication
- [Alembic](https://alembic.sqlalchemy.org/) – database migrations
- [GitHub Actions](https://github.com/features/actions) – CI/CD
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) + TypeScript – frontend *(phase 2, after the backend core)*
- [Prometheus](https://prometheus.io/) – container metrics *(planned)*

## Architecture

Wharf is built as a **modular monolith**, not microservices from day one. Core business logic — auth, the deploy engine, billing — lives as isolated Python modules with clean interfaces inside a single process, as if they were already separate services. This keeps the system simple to reason about while making it straightforward to extract any module into a real service later without rewriting the underlying logic.

The one deliberate exception is **auth**, wrapped in its own gRPC service as a hands-on exercise in inter-service communication, kept separate from the rest of the system — which stays a monolith through MVP.

### Deploy Flow
![Deploy Flow](docs/deploy-flow.png)

### Auth Flow (gRPC)
![Auth Flow](docs/auth-flow.png)

## Quick Start

```bash
git clone https://github.com/Eraliev006/wharf-platform.git
cd wharf
cp .env.example .env
docker compose up -d
```

The API will be available at `http://localhost:8000`. Full setup docs will land in `docs/` once the deploy engine is live.

## Project Structure

```
wharf/
├── app/
│   ├── auth/            # JWT + refresh rotation, wrapped as a gRPC service
│   ├── deploy_engine/   # image builds, container lifecycle
│   ├── billing_stub/    # billing placeholder module
│   └── common/          # shared interfaces, config, logging
├── migrations/          # Alembic migrations
├── docker/              # Dockerfiles, compose files
├── frontend/            # React + Vite (phase 2)
└── docs/                # architecture notes, ADRs
```

## Roadmap

Development is tracked entirely through GitHub [Issues](https://github.com/Eraliev006/wharf-platform/issues) and [Milestones](https://github.com/Eraliev006/wharf-platform/milestones) — one milestone per epic, covering infrastructure, auth, the deploy engine, networking, observability, the managed database add-on, security isolation, Git integration, the frontend, and platform self-deployment.

## License

MIT — see [LICENSE](LICENSE).
