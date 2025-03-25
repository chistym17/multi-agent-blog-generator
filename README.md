# AI Blog Generation System

A **FastAPI-based** backend system that generates blog posts using a pipeline of specialized AI agents. The system provides **real-time progress updates** through WebSocket connections.

## Features

- **Trending Topic Research**: Identifies popular topics.
- **Content Planning**: Creates structured blog outlines.
- **AI-Powered Content Generation**: Writes detailed blog posts.
- **SEO Optimization**: Enhances content for better ranking.
- **Final Review & Enhancement**: Ensures quality and coherence.
- **Real-time WebSocket Updates**: Provides live progress tracking.

## Project Structure

```
├── agents/
│   ├── research_agent.py   # Researches trending topics
│   ├── planning_agent.py   # Creates content outline
│   ├── content_agent.py    # Generates blog content
│   ├── seo_agent.py        # Optimizes for search engines
│   └── review_agent.py     # Performs final review
├── main.py                 # FastAPI server & WebSocket handler
├── .env                    # Environment variables (private)
├── .env.example            # Environment variables template
└── requirements.txt        # Project dependencies
```

## Installation & Setup

### Clone the Repository

```bash
git clone git@github.com:chistym17/multi-agent-blog-generator.git
cd  multi-agent-blog-generator
```

### Create & Activate Virtual Environment

#### On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
cp .env.example .env
```

```

## Usage
1. **Give a topic name in the generate_blog.py**
2. **python generate_blog.py**.
3. **Blog will be saved in output directory**.

```
