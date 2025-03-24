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
git clone <repository-url>
cd <project-directory>
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

### Run the Application
```bash
uvicorn main:app --reload
```

## Usage
1. **Start the FastAPI Server**
2. **Connect to WebSocket** for real-time blog generation updates.
3. **Monitor Progress** as AI agents collaboratively generate content.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).

