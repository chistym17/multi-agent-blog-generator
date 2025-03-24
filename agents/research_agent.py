from together import Together
from dotenv import load_dotenv
import os

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class ResearchAgent:
    def __init__(self):
        self.client = Together(api_key=TOGETHER_API_KEY)

    def research(self, topic="HR", year=2025, num_topics=5):
        prompt = f"""
You are an expert {topic} researcher tracking the latest trends.  
Your task is to identify the top {num_topics} trending {topic} topics for {year} and provide a brief explanation (2-3 sentences) for each.  

For each trend, highlight:  
- Why it is gaining traction.  
- Key developments or statistics.  
- A real-world example if available.  

At the end, based on relevance and impact, **choose one topic** that would be the best focus for a detailed blog post.  

Format the output as follows:  

#### **Trending {topic} Topics in {year}**  
1. **[Topic 1]**: [Brief explanation]  
2. **[Topic 2]**: [Brief explanation]  
3. **[Topic 3]**: [Brief explanation]  
4. **[Topic 4]**: [Brief explanation]  
5. **[Topic 5]**: [Brief explanation]  

#### **Final Selected Topic:**  
**[Chosen Topic]** – [Why this topic is the most relevant for a blog post]  
"""

        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,  
            temperature=0.7 
        )
        
        research_output = response.choices[0].message.content.strip()
        
        try:
            if "#### **Final Selected Topic:**" in research_output:
                topics_section, final_topic_section = research_output.split("#### **Final Selected Topic:**")
            else:
                sections = research_output.split("####")
                topics_section = sections[1]  
                final_topic_section = sections[2]  
            
            topics = []
            for line in topics_section.strip().split("\n"):
                if line.startswith(str(len(topics) + 1) + "."):
                    topic_text = line.split("**: ", 1)[1]
                    topics.append({
                        "topic": line.split("**")[1],  
                        "details": topic_text
                    })

            final_parts = final_topic_section.strip().split(" – ", 1)
            selected_topic = final_parts[0].strip().strip('**')
            selected_topic_details = final_parts[1].strip() if len(final_parts) > 1 else ""

            return {
                "trending_topics": topics,
                "selected_topic": selected_topic,
                "selected_topic_details": selected_topic_details
            }
        except Exception as e:
            print(f"Parsing error: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_output": research_output
            }
