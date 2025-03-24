import requests
from dotenv import load_dotenv
import os

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

class PlanningAgent:
    def __init__(self):
        self.api_url = "https://api.cohere.ai/v1/generate"
        self.headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        }

    def plan(self, research_data):
        selected_topic = research_data.get("selected_topic", "Unknown Topic")
        selected_topic_details = research_data.get("selected_topic_details", "No details provided.")
        
      

        prompt = f"""
Create a detailed blog outline in Markdown format for a 2000-word post on '{selected_topic}'. 
Use this research: {selected_topic_details}

Include:
1. An engaging introduction that sets the context and importance of {selected_topic}
2. 3-5 main sections with relevant subheadings
3. A conclusion with actionable takeaways
4. Each section should have:
   - Clear heading
   - 1-2 sentence description of what will be covered
   - Key points or examples to be discussed

Format the outline in proper Markdown with:
- Main sections using ## (H2)
- Subsections using ### (H3)
- Bullet points for section descriptions
- Clear hierarchy and structure

Focus on:
- Current trends and developments
- Real-world applications and examples
- Industry statistics and data points
- Best practices and strategies
- Future implications
"""

        payload = {
            "prompt": prompt,
            "max_tokens": 1000,  
            "temperature": 0.7,  
            "return_likelihoods": "NONE" 
        }

        response = requests.post(self.api_url, json=payload, headers=self.headers)
        response.raise_for_status()  

        outline = response.json()["generations"][0]["text"].strip()

        if not outline.startswith("#"):
            outline = f"# {selected_topic}\n{outline}"

        return outline

