import google.generativeai as genai

def generate_summary(text: str) -> str:
    """Generate a summary of the given text using Google Gemini."""
    prompt = f"""
    You are an AI assistant specializing in summarizing complex contractual documents for the common person who is not very sound in complex legal jargon.
    Your task is to analyze contracts and provide a clear, concise summary that avoids heavy legal jargon.

    Document text:
    {text}
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()