from openai import OpenAI

client = OpenAI()

def tone_checker(text):
    """
    Analyzes the tone of a given text and returns a classification.
    
    Parameters:
        text (str): The text to analyze.
    
    Returns:
        dict: Dictionary containing detected tone and explanation.
    """
    try:
        prompt = f"""
        Analyze the tone of the following text.
        Provide the main tone (e.g., formal, casual, persuasive, emotional, sarcastic, etc.)
        and a short explanation:
        ---
        {text}
        """
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )
        return {"tone_analysis": response.output_text.strip()}
    except Exception as e:
        return {"error": str(e)}

