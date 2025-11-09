import streamlit as st
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')

# Use a simpler, more reliable model
sentiment_pipeline = None


def get_pipeline():
    """Lazy load the pipeline to avoid initialization errors"""
    global sentiment_pipeline
    if sentiment_pipeline is None:
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        )
    return sentiment_pipeline


def detect_sentiment(text):
    """
    Analyzes the sentiment of input text.
    Returns: 'positive', 'negative', or 'neutral'
    """
    try:
        pipe = get_pipeline()
        result = pipe(text[:512])[0]  # Limit to 512 tokens

        label = result['label'].lower()
        score = result['score']

        # DistilBERT returns POSITIVE or NEGATIVE
        # Consider it neutral if confidence is low
        if score < 0.65:
            return 'neutral'
        elif 'positive' in label:
            return 'positive'
        else:
            return 'negative'

    except Exception as e:
        st.error(f"Sentiment analysis error: {e}")
        return 'neutral'