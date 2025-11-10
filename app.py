import streamlit as st
from generator import generate_text
import sentiment

st.set_page_config(page_title="Sentiment-Based Text Generator", page_icon="🤖")

st.title("🤖 Sentiment-Based Text Generator")
st.write("Enter a prompt and receive a sentiment-aligned paragraph.")

# -----------------------------
# User input
# -----------------------------
user_prompt = st.text_area("Enter your prompt:", height=120)

# -----------------------------
# Sidebar settings
# -----------------------------
st.sidebar.header("Settings")
manual_override = st.sidebar.selectbox(
    "Override Sentiment (optional):",
    ["Auto-detect", "Positive", "Negative", "Neutral"]
)

# -----------------------------
# Generate button
# -----------------------------
if st.button("Generate Text"):
    if not user_prompt.strip():
        st.error("Please enter a prompt to generate text.")
    else:
        # Detect or override sentiment
        if manual_override == "Auto-detect":
            detected_sentiment = sentiment.detect_sentiment(user_prompt)
        else:
            detected_sentiment = manual_override.lower()

        st.info(f"Detected Sentiment: {detected_sentiment.upper()}")

        # Generate paragraph
        with st.spinner("Generating paragraph..."):
            paragraph = generate_text(user_prompt, detected_sentiment)

        # Display results
        st.subheader("Generated Text:")
        st.write(paragraph)
        st.caption(f"Word count: {len(paragraph.split())}")
