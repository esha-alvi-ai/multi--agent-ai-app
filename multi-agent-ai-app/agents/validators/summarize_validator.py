from openai import OpenAI

client = OpenAI()

def summarize_validator(text, max_sentences=3):
    """
    Validates and generates a summary of the given text.
    
    Parameters:
        text (str): The text to summarize.
        max_sentences (int): Maximum sentences in the summary.
    
    Returns:
        str: Summary text.
    """
    try:
        prompt = f"""
        Summarize the following text in {max_sentences} sentences.
        Keep it concise and clear:
        ---
        {text}
        """
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )
        return response.output_text.strip()
    except Exception as e:
        return f"Error in summarization: {str(e)}"
