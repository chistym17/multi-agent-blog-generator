from agents.research_agent import ResearchAgent
from agents.planning_agent import PlanningAgent
from agents.content_agent import ContentAgent
from agents.seo_agent import SEOAgent
from agents.review_agent import ReviewAgent
import os
import json

def generate_blog():
    print("🚀 Starting blog generation pipeline...")
    
    try:
        # Step 1: Research
        print("📚 Researching topics...")
        research_agent = ResearchAgent()
        research_output = research_agent.research(topic="blockchain", year=2025, num_topics=5)
        
        # Step 2: Planning
        print("📝 Creating blog outline...")
        planning_agent = PlanningAgent()
        outline = planning_agent.plan(research_output)
        
        # Step 3: Content Generation
        print("✍️ Generating content...")
        content_agent = ContentAgent()
        content_agent.generate(outline)
        
        # Step 4: SEO Optimization
        print("🔍 Optimizing for SEO...")
        seo_agent = SEOAgent()
        seo_agent.optimize()
        
        # Step 5: Final Review
        print("👀 Performing final review...")
        review_agent = ReviewAgent()
        review_agent.final_review()
        
        print("✅ Blog generation completed! Check the output directory for files.")
        
    except Exception as e:
        print(f"❌ Error during blog generation: {str(e)}")
        raise

if __name__ == "__main__":
    generate_blog()
