from together import Together
from dotenv import load_dotenv
import os
import json

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class SEOAgent:
    def __init__(self):
        self.client = Together(api_key=TOGETHER_API_KEY)

    def read_blog_content(self, filename="blog_post.md"):
        """Read blog content from the output directory"""
        try:
            filepath = os.path.join("output", filename)
            with open(filepath, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading blog content: {str(e)}")
            return None

    def save_seo_outputs(self, seo_output):
        """Save all SEO-related outputs to files"""
        try:
            os.makedirs("output", exist_ok=True)
            
            with open("output/seo_optimized_blog.md", "w") as f:
                f.write(seo_output["optimized_content"])
            
            with open("output/schema_markup.json", "w") as f:
                f.write(seo_output["schema_markup"])
            
            with open("output/keyword_analysis.json", "w") as f:
                json.dump(seo_output["keywords"], f, indent=2)
            
            print("SEO outputs saved successfully to output directory")
            return True
        except Exception as e:
            print(f"Error saving SEO outputs: {str(e)}")
            return False

    def analyze_keywords(self, blog_content):
        """Analyze blog content to determine optimal keywords"""
        keyword_prompt = f"""
        Analyze this blog content and extract SEO keywords. Return ONLY a JSON object in this exact format:
        {{
            "primary_keyword": "main topic keyword",
            "secondary_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
            "lsi_keywords": ["related1", "related2", "related3", "related4", "related5", "related6", "related7", "related8"]
        }}

        Blog content:
        {blog_content}

        Remember: Return ONLY the JSON object, no additional text or explanation.
        """

        try:
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=[{"role": "user", "content": keyword_prompt}],
                max_tokens=1000,
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()
            
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()

            keywords = json.loads(content)
            
            required_keys = ['primary_keyword', 'secondary_keywords', 'lsi_keywords']
            if not all(key in keywords for key in required_keys):
                raise ValueError("Missing required keys in keyword analysis")
                
            return keywords

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {content}")
            return {
                "primary_keyword": "blog topic",
                "secondary_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
                "lsi_keywords": ["related1", "related2", "related3", "related4", "related5"]
            }
        except Exception as e:
            print(f"Unexpected error in keyword analysis: {e}")
            return {
                "primary_keyword": "blog topic",
                "secondary_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
                "lsi_keywords": ["related1", "related2", "related3", "related4", "related5"]
            }

    def optimize(self, blog_content=None):
        if blog_content is None:
            blog_content = self.read_blog_content()
            if blog_content is None:
                raise ValueError("No blog content provided or found in output directory")

        keywords = self.analyze_keywords(blog_content)
        
        seo_prompt = f"""
        Enhance this blog post for SEO while maintaining its professional tone and readability.
        
        Primary keyword: {keywords['primary_keyword']}
        Secondary keywords: {', '.join(keywords['secondary_keywords'])}
        LSI keywords: {', '.join(keywords['lsi_keywords'])}
        
        Please:
        1. Add an SEO-optimized meta description (155 characters max) using the primary keyword
        2. Optimize headings with relevant keywords (H1 should contain primary keyword)
        3. Add internal linking suggestions based on the topic and keywords
        4. Naturally incorporate all keywords throughout the content
        5. Enhance readability with:
           - Shorter paragraphs (3-4 sentences max)
           - Bullet points for lists
           - Transition sentences
           - Strategic keyword placement (especially in first/last paragraphs)
        6. Add a table of contents
        7. Include relevant statistics and data points
        8. Add strategic CTAs that align with the content topic
        9. Suggest relevant meta tags
        
        Original content:
        {blog_content}
        """

        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": seo_prompt}],
            max_tokens=3000,
            temperature=0.5
        )

        optimized_content = response.choices[0].message.content.strip()

        schema_prompt = f"""
        Create JSON-LD schema markup for this blog post. Include:
        1. Article schema (using primary keyword: {keywords['primary_keyword']})
        2. Organization schema
        3. BreadcrumbList schema
        4. FAQPage schema (generate 3-4 relevant FAQs based on the content)

        Blog content first paragraph:
        {blog_content[:500]}...
        
        Keywords to incorporate:
        Primary: {keywords['primary_keyword']}
        Secondary: {', '.join(keywords['secondary_keywords'])}
        """

        schema_response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": schema_prompt}],
            max_tokens=1000,
            temperature=0.3
        )

        schema_markup = schema_response.choices[0].message.content.strip()

        final_output = {
            "keywords": keywords,
            "optimized_content": optimized_content,
            "schema_markup": schema_markup
        }
        
        self.save_seo_outputs(final_output)
        
        return final_output

