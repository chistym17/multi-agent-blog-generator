from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import Optional
import asyncio

from agents.research_agent import ResearchAgent
from agents.planning_agent import PlanningAgent
from agents.content_agent import ContentAgent
from agents.seo_agent import SEOAgent
from agents.review_agent import ReviewAgent

app = FastAPI()

class BlogRequest(BaseModel):
    topic: str
    additional_info: Optional[dict] = None

async def heartbeat(websocket: WebSocket):
    while True:
        try:
            await asyncio.sleep(30)  
            await websocket.send_json({"type": "ping"})
        except Exception:
            break

async def generate_blog_with_updates(websocket: WebSocket, topic: str):
    steps = [
        {
            "step": 1,
            "agent": "Research Agent",
            "status": "researching",
            "message": "Gathering comprehensive data on the topic...",
            "estimated_time": "30-45 seconds"
        },
        {
            "step": 2,
            "agent": "Planning Agent",
            "status": "planning",
            "message": "Creating structured outline and content plan...",
            "estimated_time": "20-30 seconds"
        },
        {
            "step": 3,
            "agent": "Content Agent",
            "status": "writing",
            "message": "Generating engaging blog content...",
            "estimated_time": "60-90 seconds"
        },
        {
            "step": 4,
            "agent": "SEO Agent",
            "status": "optimizing",
            "message": "Optimizing content for search engines...",
            "estimated_time": "20-30 seconds"
        },
        {
            "step": 5,
            "agent": "Review Agent",
            "status": "reviewing",
            "message": "Performing final review and polish...",
            "estimated_time": "30-45 seconds"
        }
    ]

    try:
        heartbeat_task = asyncio.create_task(heartbeat(websocket))

        await websocket.send_json({
            **steps[0],
            "progress": 0
        })
        research_agent = ResearchAgent()
        research_output = research_agent.research(topic=topic, year=2025, num_topics=5)

        await websocket.send_json({
            **steps[1],
            "progress": 20
        })
        planning_agent = PlanningAgent()
        outline = planning_agent.plan(research_output)

        await websocket.send_json({
            **steps[2],
            "progress": 40
        })
        content_agent = ContentAgent()
        content_agent.generate(outline)
        
        await websocket.send_json({
            **steps[3],
            "progress": 70
        })
        seo_agent = SEOAgent()
        seo_agent.optimize()
        
        await websocket.send_json({
            **steps[4],
            "progress": 90
        })
        review_agent = ReviewAgent()
        final_content = review_agent.final_review()

        await websocket.send_json({
            "step": 6,
            "status": "completed",
            "message": "Blog post generated successfully!",
            "progress": 100,
            "content": final_content
        })

    except Exception as e:
        await websocket.send_json({
            "status": "error",
            "message": str(e)
        })
    finally:
        heartbeat_task.cancel()

@app.websocket("/ws/generate-blog")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        await generate_blog_with_updates(websocket, data["topic"])
    except Exception as e:
        await websocket.send_json({
            "status": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()