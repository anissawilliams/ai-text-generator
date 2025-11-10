import random
from sentiment import detect_sentiment  # import your sentiment detection

# Helper functions
def extract_topic_keywords(prompt: str) -> str:
    stop_words = {
        'i','me','my','we','our','you','your','he','she','it','they',
        'am','is','are','was','were','be','been','being',
        'have','has','had','do','does','did',
        'a','an','the','and','or','but','if','because',
        'as','what','which','this','that','these','those',
        'love','hate','like','think','feel','believe',
        'how','why','when','where','who'
    }
    words = prompt.lower().split()
    keywords = [w.strip('.,!?;:') for w in words if w.strip('.,!?;:') not in stop_words]
    return ' '.join(keywords[:5]) if words else prompt

def classify_topic_type(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["pizza","ice cream","burger","food","meal","snack","dish"]):
        return "food"
    elif any(word in prompt_lower for word in ["beach","soccer","game","playing","travel","vacation","hobby"]):
        return "activity"
    elif any(word in prompt_lower for word in ["dog","cat","pet","animal","bird","fish"]):
        return "animal"
    else:
        return "generic"

# Rule-based paragraph templates
TEMPLATES = {
    # ... same as in the final generator.py we wrote earlier ...
}

def generate_rule_based_paragraph(prompt: str, sentiment: str) -> str:
    topic_type = classify_topic_type(prompt)
    sentences = TEMPLATES[topic_type].get(sentiment, TEMPLATES["generic"]["neutral"])
    random.shuffle(sentences)
    return " ".join(sentences)

def generate_text(prompt: str, sentiment: str = None) -> str:
    """Generate a sentiment-aligned paragraph."""
    if sentiment is None or sentiment.lower() == "auto":
        sentiment = detect_sentiment(prompt)
    return generate_rule_based_paragraph(prompt, sentiment)
