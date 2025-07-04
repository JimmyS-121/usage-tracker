# AI Usage Tracker (Python)

A Python FastAPI implementation for tracking staff usage of AI tools.

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file
4. Run the server: `uvicorn main:app --reload`

## API Documentation

After starting the server, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Deployment

### Option 1: Docker
1. Build: `docker build -t ai-usage-tracker .`
2. Run: `docker run -p 8000:8000 --env-file .env ai-usage-tracker`

### Option 2: Render.com
1. Create new Web Service
2. Connect your GitHub repository
3. Set environment variables
4. Deploy

### Option 3: Railway.app
1. Create new project
2. Import from GitHub
3. Add PostgreSQL service
4. Set environment variables
5. Deploy
