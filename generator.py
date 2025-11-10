import streamlit as st
import anthropic
from sentiment import detect_sentiment

# Initialize the Anthropic client using Streamlit secrets
api_key = st.secrets.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in Streamlit secrets")

client = anthropic.Anthropic(api_key=api_key)

def generate_text(prompt: str, sentiment: str = None) -> str:
    """
    Generate a sentiment-aligned paragraph for the given prompt using Claude Haiku.
    If sentiment is None or 'auto', detect it using sentiment.py.
    """
    if sentiment is None or sentiment.lower() == "auto":
        sentiment = detect_sentiment(prompt)

    # Build the system prompt to guide the model
    system_prompt = f"""You are a thoughtful and nuanced writer. 
Generate a single, well-written paragraph (3-4 sentences) that discusses the following topic.
The tone should be {sentiment}.
Keep the paragraph concise and engaging."""

    # Make the API call using Claude Haiku (fastest, cheapest model)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        system=system_prompt
    )

    # Extract the text from the response
    return message.content[0].text