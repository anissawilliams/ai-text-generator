
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

# Initialize sentiment analyzer (using a better model)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    top_k=None
)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of input text.
    Returns: 'positive', 'negative', or 'neutral'
    """
    try:
        results = sentiment_pipeline(text)[0]

        # The model returns labels like 'positive', 'negative', 'neutral'
        # Find the label with highest score
        top_result = max(results, key=lambda x: x['score'])
        label = top_result['label'].lower()

        # Map labels to our three categories
        if 'pos' in label:
            return 'positive'
        elif 'neg' in label:
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 'neutral'  # Default fallback

# Alternative: If you want to use the original DistilBERT model
def analyze_sentiment_simple(text):
    """Simpler sentiment analyzer using DistilBERT"""
    from transformers import pipeline

    analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    )

    result = analyzer(text)[0]
    label = result['label'].lower()

    # This model only returns POSITIVE or NEGATIVE
    # We'll consider neutral if score is close to 0.5
    if result['score'] < 0.6:
        return 'neutral'
    return label
