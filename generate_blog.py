from agents.research_agent import ResearchAgent
from agents.planning_agent import PlanningAgent
from agents.content_agent import ContentAgent
from agents.seo_agent import SEOAgent
from agents.review_agent import ReviewAgent

def generate_blog():
    # Hardcoded topic
    topic = "Artificial Intelligence in Healthcare"
    
    print("\n🚀 Starting Blog Generation Process...")
    print(f"📝 Topic: {topic}\n")

    try:
        print("Step 1: Research Phase")
        print("🔍 Research Agent: Gathering comprehensive data on the topic...")
        research_agent = ResearchAgent()
        research_output = research_agent.research(topic=topic, year=2025, num_topics=5)
        print("✅ Research completed!\n")

        # Step 2: Planning
        print("Step 2: Planning Phase")
        print("📋 Planning Agent: Creating structured outline...")
        planning_agent = PlanningAgent()
        outline = planning_agent.plan(research_output)
        print("✅ Outline created!\n")

        # Step 3: Content Generation
        print("Step 3: Content Generation Phase")
        print("✍️ Content Agent: Generating engaging blog content...")
        content_agent = ContentAgent()
        content_agent.generate(outline)
        print("✅ Content generated!\n")

        # Step 4: SEO Optimization
        print("Step 4: SEO Optimization Phase")
        print("🎯 SEO Agent: Optimizing content for search engines...")
        seo_agent = SEOAgent()
        seo_agent.optimize()
        print("✅ SEO optimization completed!\n")

        # Step 5: Final Review
        print("Step 5: Review Phase")
        print("👀 Review Agent: Performing final review and polish...")
        review_agent = ReviewAgent()
        final_content = review_agent.final_review()
        print("✅ Final review completed!\n")

        # Final Output
        print("🎉 Blog Generation Completed Successfully!")
        print("\n=== Final Blog Content saved in output directory ===")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    generate_blog()