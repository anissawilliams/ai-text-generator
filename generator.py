import streamlit as st
import anthropic
from sentiment import detect_sentiment

# api_key = st.secrets.get("ANTHROPIC_API_KEY")
# st.write(f"Key found: {bool(api_key)}")
# st.write(f"Key length: {len(api_key) if api_key else 0}")
# st.write(f"Key starts with: {api_key[:10] if api_key else 'None'}...")
# Initialize the Anthropic client using Streamlit secrets
api_key = st.secrets.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in Streamlit secrets")

client = anthropic.Anthropic(api_key=api_key)
try:
    # Test with a simple call
    test_message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    st.success("API key works!")
except anthropic.AuthenticationError as e:
    st.error(f"Auth error: Check if key is valid and active")
    st.error(f"Key starts with: {api_key[:15]}...")  # Show first 15 chars only
except Exception as e:
    st.error(f"Other error: {type(e).__name__}")

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