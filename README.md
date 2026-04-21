# QA Analytics Platform

Self-hosted full-stack platform for collecting, storing, analyzing, and visualizing automated test results with future AI-agent extensions.

---

# Overview

QA Analytics Platform is an engineering project focused on real QA workflows.

The platform collects results from automated tests, stores historical executions, analyzes quality trends, detects unstable tests, and provides a dashboard for visibility.

It is designed to evolve into a system that combines:

- classical QA automation
- analytics engineering
- CI/CD integrations
- AI-assisted quality analysis
- exploratory AI agents

---

# What Is Already Implemented

## Backend Platform

- FastAPI REST API
- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- modular architecture

## Core Entities

- `projects`
- `test_runs`
- `test_results`

## Analytics

- summary metrics
- pass rate
- top failures
- flaky tests detection
- project-level metrics

## UI Dashboard

- HTML dashboard via Jinja2
- metrics cards
- pass/fail distribution chart
- top failures section
- flaky tests section
- recent test runs table

## Ingestion Pipelines

### Manual ingestion

- Postman requests

### Pytest ingestion

- parse real `pytest-json-report`
- upload runs + test results

### Selenium ingestion

- UI tests executed with Selenium
- results exported to JSON
- uploaded into platform

## Demo Test Target

Built-in demo web app:

- login page
- successful login flow
- failed login flow

Used as Selenium test target.

---

# Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Jinja2
- Selenium
- Pytest
- Docker Compose
- Postman

---

# Current Architecture

pytest / selenium / postman
        ↓
 JSON reports / API calls
        ↓
     FastAPI Backend
        ↓
 SQLAlchemy + PostgreSQL
        ↓
 Analytics Endpoints
        ↓
 Dashboard UI