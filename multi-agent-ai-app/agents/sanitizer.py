import os
import openai
from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY="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"
openai.api_key = os.getenv("OPENAI_API_KEY")

class SanitizerAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def sanitize_text(self, text: str) -> str:
        """
        Sanitize the text by removing profanity, inappropriate content,
        fixing grammar, and returning only the cleaned version.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a text sanitization assistant. "
                            "Remove any inappropriate, offensive, or irrelevant content. "
                            "Fix grammar and spelling mistakes. "
                            "Return only the sanitized text, with no extra commentary."
                        )
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=1000,
                n=1,
            )

            return response.choices[0].message["content"].strip()

        except Exception as e:
            print(f"An error occurred during sanitization: {e}")
            return None
