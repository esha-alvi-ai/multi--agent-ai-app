import openai
from config import OPRNAI_API_KEY
openai.api_key = OPRNAI_API_KEY



OPENAI_API_KEY="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"
class WriterAgent:
    def __init__(self, model="gpt-4o"):
        self.model = model

    def generate_article(self, prompt: str, tone: str = "professional", length: str = "medium") -> str:
        """
        Generate a detailed article from the given prompt.
        """
        length_map = {
            "short": "around 100 words",
            "medium": "around 300 words",
            "long": "around 600 words"
        }

        system_prompt = (
            f"You are a professional article writer. "
            f"Write a {length_map.get(length, 'medium length')} article in a {tone} tone "
            f"based on the following prompt: {prompt}"
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            return response.choices[0].message["content"].strip()

        except Exception as e:
            print(f"An error occurred while generating the article: {e}")
            return None

