# GreenLens AI

GreenLens AI is a full-stack portfolio project for AI-assisted plant image analysis.

Users can upload plant images, create analysis jobs, trigger image processing, and retrieve normalized analysis results. The application is built with a separated backend and AI service architecture. The AI service currently returns mock analysis data and is prepared to be extended with the Pl@ntNet REST API.

## Project Goal

This project demonstrates a realistic full-stack application architecture with:

* image upload handling
* asynchronous-style job processing
* job status management
* communication between separate backend and AI services
* structured JSON result storage
* REST API design with FastAPI
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
* result storage as `result.json`
* result retrieval endpoint

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
* analyzing the image
* returning normalized analysis results
* later connecting to the Pl@ntNet REST API

## Project Structure

```
greenlens-ai/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  └─ services/
│  │     └─ __init__.py
│  ├─ data/
│  │  └─ jobs/
│  └─ requirements.txt
│
├─ ai-service/
│  ├─ app/
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

```text
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

8. Retrieve the stored analysis result with:

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

* refactor backend code into smaller modules
* move job-related endpoints into a dedicated router
* move file and status handling into a job storage service
* move AI service communication into a dedicated client module
* replace mock AI results with Pl@ntNet API integration
* add React frontend with upload form and result view
* add SQLite persistence
* add tests with pytest
* add Docker and Docker Compose
* improve README with screenshots and architecture diagram

## Notes

This project is built as a learning and portfolio project. The current AI result is mocked. The planned Pl@ntNet integration will be added in a later step.

API keys and local environment files must not be committed to the repository.
