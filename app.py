import streamlit as st
import sentiment
import generator

st.set_page_config(page_title="AI Sentiment Text Generator", page_icon="🤖", layout="wide")

st.title("🤖 AI Sentiment-Based Text Generator")
st.markdown("Enter a prompt and the AI will detect its sentiment, then generate aligned content.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    word_count = st.slider("Target Word Count", 50, 500, 150, 25)
    manual_override = st.selectbox(
        "Manual Sentiment Override (Optional)",
        ["Auto-detect", "Positive", "Negative", "Neutral"]
    )
    st.markdown("---")
    st.markdown("### How It Works")
    st.markdown("1. 📝 Enter your prompt")
    st.markdown("2. 🧠 AI analyzes sentiment")
    st.markdown("3. ✨ Generates aligned text")

# Main input
user_prompt = st.text_area(
    "Enter your prompt:",
    height=150,
    placeholder="e.g., 'I love how technology connects people' or 'The rising cost of living is concerning'"
)

if st.button("🚀 Analyze & Generate", type="primary", use_container_width=True):
    if not user_prompt.strip():
        st.error("Please enter a prompt!")
    else:
        with st.spinner("🧠 Analyzing sentiment..."):
            # Detect sentiment
            if manual_override == "Auto-detect":
                detected_sentiment = sentiment.analyze_sentiment(user_prompt)
            else:
                detected_sentiment = manual_override.lower()

            # Display sentiment
            sentiment_colors = {
                "positive": "🟢",
                "negative": "🔴",
                "neutral": "🔵"
            }
            st.success(
                f"{sentiment_colors.get(detected_sentiment, '⚪')} Detected Sentiment: **{detected_sentiment.upper()}**")

        with st.spinner("✨ Generating text..."):
            # Generate text
            generated_text = generator.generate_text(
                user_prompt,
                detected_sentiment,
                word_count
            )

            # Display result
            st.markdown("### 📄 Generated Text")
            st.markdown(
                f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #1f77b4;'>{generated_text}</div>",
                unsafe_allow_html=True)

            actual_word_count = len(generated_text.split())
            st.caption(f"Word count: {actual_word_count} words")