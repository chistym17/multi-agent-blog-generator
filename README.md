# AI Blog Generation System

A FastAPI-based backend system that generates blog posts using a pipeline of specialized AI agents. The system provides real-time progress updates through WebSocket connections.

## Project Structure

├── agents/
│ ├── research_agent.py # Researches trending topics
│ ├── planning_agent.py # Creates content outline
│ ├── content_agent.py # Generates blog content
│ ├── seo_agent.py # Optimizes for search engines
│ └── review_agent.py # Performs final review
├── main.py # FastAPI server & WebSocket handler
├── .env # Environment variables (private)
├── .env.example # Environment variables template
└── requirements.txt # Project dependencies
bash
git clone <repository-url>
cd <project-directory>
bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
bash
pip install -r requirements.txt
bash
cp .env.example .env
bash
uvicorn main:app --reload
