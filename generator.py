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
    Generate a sentiment-aligned paragraph for the given prompt using Claude Sonnet.
    If sentiment is None or 'auto', detect it using sentiment.py.
    """
    if sentiment is None or sentiment.lower() == "auto":
        sentiment = detect_sentiment(prompt)

    # Build a more specific, high-quality system prompt
    system_prompt = f"""You are an expert writer who creates compelling, nuanced content.

Write a single well-crafted paragraph (4-6 sentences) about the given topic.
- Tone: {sentiment}
- Style: Engaging and substantive with vivid details
- Avoid generic statements; be specific and insightful
- Use varied sentence structure for better flow"""

    # Use Sonnet 4.5 for much better quality
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Upgraded from Haiku
        max_tokens=500,  # Increased for better completions
        temperature=0.7,  # Adds creativity while staying coherent
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        system=system_prompt
    )

    return message.content[0].text