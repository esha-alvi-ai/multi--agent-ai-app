import openai
from config import OPRNAI_API_KEY
openai.api_key = OPRNAI_API_KEY



OPENAI_API_KEY="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"
class SummarizationAgent:
    def __init__(self, model="gpt-3.5-turbo", max_tokens=300):
        self.model = model
        self.max_tokens = max_tokens

    def summarize(self, input_text: str, objective: str = "Summarize the text in a concise manner.") -> str:
        """
        Summarizes the input text based on the provided objective.
        """
        if not input_text or not isinstance(input_text, str):
            return "[No input provided to summarize.]"

        prompt = (
            f"{objective}\n\n"
            f"Content:\n{input_text}\n\n"
            f"Summarized Content:"
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message["content"].strip()

        except Exception as e:
            print(f"An error occurred during summarization: {e}")
            return None
