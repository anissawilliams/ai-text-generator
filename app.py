
import streamlit as st
import sentiment
import generator

st.write("🔑 Key prefix:", st.secrets.get("ANTHROPIC_API_KEY", "Not found")[:12])

st.title("AI Sentiment-Based Text Generator")

st.write("Enter a prompt and the AI will detect its sentiment and generate aligned text.")

# Input
user_prompt = st.text_area("Enter your prompt:", height=100)

# Settings
#st.sidebar.header("Settings")
#word_count = st.sidebar.number_input("Word Count", min_value=50, max_value=500, value=150)
#manual_override = st.sidebar.selectbox("Override Sentiment", ["Auto-detect", "Positive", "Negative", "Neutral"])
# col1, col2 = st.columns(2)
# with col1:
#     word_count = st.number_input("Word Count", min_value=50, max_value=500, value=150)
# with col2:
#     manual_override = st.selectbox("Override Sentiment", ["Auto-detect", "Positive", "Negative", "Neutral"])

# Generate button
if st.button("Generate Text"):
    if user_prompt:
        # Detect sentiment
        detected_sentiment = sentiment.detect_sentiment(user_prompt)

        st.info(f"Detected Sentiment: {detected_sentiment.upper()}")

        # Generate text
        with st.spinner("Generating..."):
            generated_text = generator.generate_text(user_prompt, detected_sentiment)

        st.subheader("Generated Text:")
        st.write(generated_text)
        st.caption(f"Word count: {len(generated_text.split())}")
    else:
        st.error("Please enter a prompt")