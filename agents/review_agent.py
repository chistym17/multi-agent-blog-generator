from together import Together
from dotenv import load_dotenv
import os
import json

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class ReviewAgent:
    def __init__(self):
        self.client = Together(api_key=TOGETHER_API_KEY)

    def check_markdown_structure(self, content):
        """Verify and fix markdown structure"""
        structure_prompt = f"""
        Review and fix the markdown structure of this blog post. Return ONLY the corrected markdown content with:
        1. Proper heading hierarchy (H1 > H2 > H3)
        2. Consistent formatting for lists and bullet points
        3. Proper spacing between sections
        4. Correct markdown syntax for links and emphasis
        5. Clean, organized table of contents
        
        Content to review:
        {content}
        """

        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": structure_prompt}],
            max_tokens=3000,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()

    def enhance_content_quality(self, content):
        """Improve content quality and readability"""
        quality_prompt = f"""
        Enhance this blog post's quality. Focus on:
        1. Clarity and conciseness
        2. Professional tone
        3. Engaging transitions
        4. Active voice
        5. Industry-specific terminology
        6. Data-backed statements
        7. Actionable insights
        
        Content to enhance:
        {content}
        """

        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": quality_prompt}],
            max_tokens=3000,
            temperature=0.4
        )
        
        return response.choices[0].message.content.strip()

    def generate_improvement_suggestions(self, content):
        """Generate suggestions for further improvements"""
        suggestion_prompt = f"""
        Analyze this blog post and provide specific suggestions for improvement in JSON format:
        {{
            "content_suggestions": [
                "suggestion1",
                "suggestion2",
                ...
            ],
            "seo_suggestions": [
                "suggestion1",
                "suggestion2",
                ...
            ],
            "engagement_suggestions": [
                "suggestion1",
                "suggestion2",
                ...
            ]
        }}

        Blog content:
        {content}
        """

        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": suggestion_prompt}],
            max_tokens=1000,
            temperature=0.4
        )

        try:
            return json.loads(response.choices[0].message.content.strip())
        except json.JSONDecodeError:
            return {
                "content_suggestions": ["Review content structure", "Add more examples"],
                "seo_suggestions": ["Check keyword density", "Add more internal links"],
                "engagement_suggestions": ["Include call-to-actions", "Add reader questions"]
            }

    def read_blog_content(self, filename="seo_optimized_blog.md"):
        """Read blog content from the output directory"""
        try:
            filepath = os.path.join("output", filename)
            with open(filepath, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading blog content: {str(e)}")
            return None

    def save_review_outputs(self, review_output):
        """Save all review-related outputs to files"""
        try:
            os.makedirs("output", exist_ok=True)
            
            with open("output/final_blog.md", "w") as f:
                f.write(review_output["final_content"])
            
            with open("output/improvement_suggestions.json", "w") as f:
                json.dump(review_output["improvement_suggestions"], f, indent=2)
            
            print("Review outputs saved successfully to output directory")
            return True
        except Exception as e:
            print(f"Error saving review outputs: {str(e)}")
            return False

    def final_review(self, blog_content=None):
        """Perform final review and enhancement of the blog post"""
        try:
            if blog_content is None:
                blog_content = self.read_blog_content()
                if blog_content is None:
                    raise ValueError("No blog content provided or found in output directory")

            structured_content = self.check_markdown_structure(blog_content)
            
            enhanced_content = self.enhance_content_quality(structured_content)
            
            suggestions = self.generate_improvement_suggestions(enhanced_content)
            
            final_check_prompt = f"""
            Perform a final quality check on this blog post. Return ONLY the final blog content without any additional commentary or notes.
            Ensure:
            1. All sections are properly connected
            2. No redundant information
            3. Clear and professional tone throughout
            4. Proper formatting and structure
            5. SEO elements are well-integrated
            6. No review comments or notes in the output
            
            Content:
            {enhanced_content}
            """

            final_response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=[{"role": "user", "content": final_check_prompt}],
                max_tokens=3000,
                temperature=0.3
            )

            final_content = final_response.choices[0].message.content.strip()

            if "After conducting a thorough review" in final_content:
                final_content = final_content.split("\n\n", 1)[1]
            
            if "I made the following adjustments:" in final_content:
                final_content = final_content.split("I made the following adjustments:")[0].strip()

            review_output = {
                "final_content": final_content,
                "improvement_suggestions": suggestions,
                "status": "success"
            }

            self.save_review_outputs(review_output)

            return review_output

        except Exception as e:
            error_output = {
                "final_content": blog_content,
                "improvement_suggestions": {
                    "content_suggestions": ["Review failed - please check manually"],
                    "seo_suggestions": ["Review failed - please check manually"],
                    "engagement_suggestions": ["Review failed - please check manually"]
                },
                "status": "error",
                "error": str(e)
            }
            
            self.save_review_outputs(error_output)
            
            return error_output

