# GreenLens AI

GreenLens AI is a full-stack portfolio project for AI-assisted plant image analysis.

Users can upload plant images, create analysis jobs, trigger image processing, and retrieve normalized analysis results. The application is built with a separated backend and AI service architecture. The AI service currently returns mock analysis data and is prepared to be extended with the Pl@ntNet REST API.

## Project Goal

This project demonstrates a realistic full-stack application architecture with:

* image upload handling
* job-based processing workflow
* visible job status transitions
* communication between separate backend and AI services
* structured JSON status and result storage
* REST API design with FastAPI
* modular backend structure with routers and services
* preparation for an external AI API integration
* later frontend integration with React and TypeScript

The project is intentionally public and independent. It does not contain code or content from non-public training or internship projects.

## Current Status

Work in progress.

Currently implemented:

* FastAPI backend
* separate FastAPI AI service
* health endpoints for both services
* image upload endpoint
* job creation with UUID
* local file storage for uploaded images
* job status stored as `status.json`
* processing endpoint that calls the AI service
* mock AI analysis result
* mock processing delay to make the `processing` status visible
* result storage as `result.json`
* result retrieval endpoint
* backend router/service structure
* AI service router/service structure

Not implemented yet:

* Pl@ntNet API integration
* React frontend
* SQLite database
* Docker / Docker Compose
* automated tests
* production-ready error handling
* deployment

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* httpx
* python-multipart

### AI Service

* Python
* FastAPI
* Uvicorn
* httpx
* python-multipart

### Frontend

Planned:

* React
* Vite
* TypeScript

### External API

Planned:

* Pl@ntNet REST API

## Architecture

Current local architecture:

```
Frontend (planned)
        |
        v
Backend API
FastAPI, port 8000
        |
        v
AI Service
FastAPI, port 8001
        |
        v
Pl@ntNet API (planned)
```

The backend is responsible for:

* accepting image uploads
* creating jobs
* storing uploaded files
* managing job status
* calling the AI service
* storing and returning analysis results

The AI service is responsible for:

* accepting an image from the backend
* validating supported image types
* returning normalized analysis results
* simulating processing time during mock analysis
* later connecting to the Pl@ntNet REST API

## Project Structure

```
greenlens-ai/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ __init__.py
│  │  │  └─ jobs.py
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  ├─ ai_service_client.py
│  │  │  └─ job_storage.py
│  │  ├─ __init__.py
│  │  └─ main.py
│  ├─ data/
│  │  └─ jobs/
│  └─ requirements.txt
│
├─ ai-service/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ __init__.py
│  │  │  └─ analysis.py
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  └─ mock_analyzer.py
│  │  └─ main.py
│  └─ requirements.txt
│
├─ frontend/
├─ docs/
├─ README.md
├─ .gitignore
└─ .venv/
```

Note: `backend/data/`, `.venv/`, `.env`, and generated files are ignored by Git.

## Backend Structure

The backend is split into a small application entry point, API router, and service modules.

```
backend/app/main.py
```

Creates the FastAPI application, includes the jobs router, and provides the `/health` endpoint.

```
backend/app/api/jobs.py
```

Contains the job-related API endpoints and coordinates the job workflow.

```
backend/app/services/job_storage.py
```

Handles local job storage, including uploaded input files, `status.json`, and `result.json`.

```
backend/app/services/ai_service_client.py
```

Handles the HTTP request from the backend to the separate AI service.

## AI Service Structure

The AI service is also split into an application entry point, API router, and service module.

```
ai-service/app/main.py
```

Creates the FastAPI application, includes the analysis router, and provides the `/health` endpoint.

```
ai-service/app/api/analysis.py
```

Contains the `/analyze` endpoint and validates uploaded image types.

```
ai-service/app/services/mock_analyzer.py
```

Provides the current mock analysis response and a short artificial delay to simulate processing time.

## API Endpoints

### Backend

Base URL:

```
http://127.0.0.1:8000
```

Endpoints:

```
GET  /health
POST /jobs
GET  /jobs/{job_id}
POST /jobs/{job_id}/process
GET  /jobs/{job_id}/result
```

### AI Service

Base URL:

```
http://127.0.0.1:8001
```

Endpoints:

```
GET  /health
POST /analyze
```

## Local Setup

### 1. Clone the repository

```
git clone https://github.com/anjarud/greenlens-ai.git
cd greenlens-ai
```

### 2. Create and activate a virtual environment

```
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install backend dependencies

```
pip install -r backend/requirements.txt
```

### 4. Install AI service dependencies

```
pip install -r ai-service/requirements.txt
```

## Running the Application Locally

The backend and AI service must run in two separate terminals.

### Terminal 1: Start the AI service

```
cd D:\dev\greenlens-ai\ai-service
uvicorn app.main:app --reload --port 8001
```

AI service health check:

```
http://127.0.0.1:8001/health
```

AI service Swagger UI:

```
http://127.0.0.1:8001/docs
```

### Terminal 2: Start the backend

```
cd D:\dev\greenlens-ai
uvicorn backend.app.main:app --reload --port 8000
```

Backend health check:

```
http://127.0.0.1:8000/health
```

Backend Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Current Workflow

1. Start the AI service on port `8001`.
2. Start the backend on port `8000`.
3. Open the backend Swagger UI:

```
http://127.0.0.1:8000/docs
```

4. Upload an image with:

```
POST /jobs
```

5. Copy the returned `job_id`.

6. Check the job status with:

```
GET /jobs/{job_id}
```

7. Trigger processing with:

```
POST /jobs/{job_id}/process
```

8. During processing, the job status is temporarily set to:

```
processing
```

9. Retrieve the stored analysis result with:

```
GET /jobs/{job_id}/result
```

## Example Job Status

```
{
  "job_id": "example-job-id",
  "status": "uploaded",
  "message": "Image uploaded successfully.",
  "original_filename": "plant.jpg",
  "stored_filename": "original.jpg",
  "content_type": "image/jpeg"
}
```

## Example Mock Result

```
{
  "provider": "mock",
  "original_filename": "original.jpg",
  "results": [
    {
      "scientific_name": "Monstera deliciosa",
      "common_name": "Swiss cheese plant",
      "confidence": 0.87
    },
    {
      "scientific_name": "Epipremnum aureum",
      "common_name": "Golden pothos",
      "confidence": 0.09
    },
    {
      "scientific_name": "Philodendron hederaceum",
      "common_name": "Heartleaf philodendron",
      "confidence": 0.04
    }
  ]
}
```

## Roadmap

Planned next steps:

* prepare AI service for Pl@ntNet integration
* add configuration for external service URLs and API keys
* replace mock AI results with Pl@ntNet API integration
* add React frontend with upload form and result view
* add SQLite persistence
* add tests with pytest
* add Docker and Docker Compose
* improve error handling
* improve README with screenshots and architecture diagram

## Notes

This project is built as a learning and portfolio project. The current AI result is mocked. The planned Pl@ntNet integration will be added in a later step.

The current processing workflow is request-based: the backend starts processing when `POST /jobs/{job_id}/process` is called and waits for the AI service response. A more advanced background processing approach may be added later.

API keys and local environment files must not be committed to the repository.
