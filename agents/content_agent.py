from together import Together
from dotenv import load_dotenv
import os

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class ContentAgent:
    def __init__(self):
        self.client = Together(api_key=TOGETHER_API_KEY)

    def save_blog_content(self, blog_content):
        """Save the generated blog content to a file"""
        try:
            os.makedirs("output", exist_ok=True)
            
            filepath = os.path.join("output", "blog_post.md")
            with open(filepath, "w") as f:
                f.write(blog_content)
            
            print(f"Blog content saved successfully to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving blog content: {str(e)}")
            return False

    def generate(self, outline):
        sections = outline.split("\n## ")
        full_blog = []

        for section in sections:
            if not section.strip():
                continue

            if not section.startswith("#"):
                section = "## " + section

            lines = section.strip().split("\n")
            heading = lines[0].strip()  
            description = "\n".join(line for line in lines[1:] if line.strip()) 

            if "Introduction" in heading or "Conclusion" in heading:
                word_count = 250
                max_tokens = 600  
            else:
                word_count = 400  
                max_tokens = 1000  

            prompt = f"""
            Write a detailed section for a blog post in Markdown format based on this {outline}:  
            {heading}  
            {description}  
            Expand this into {word_count} words of professional, HR-focused content. 
            Include relevant trends, strategies, or examples as needed, ensuring the text is engaging and informative.
            """

            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7  
            )

            section_content = response.choices[0].message.content.strip()
            full_blog.append(section_content)

        final_blog = "\n\n".join(full_blog)
        
        self.save_blog_content(final_blog)
        
        return final_blog

