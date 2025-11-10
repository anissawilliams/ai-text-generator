import random
from sentiment import detect_sentiment  # your sentiment.py

# -----------------------------
# Helper functions
# -----------------------------
def classify_topic_type(prompt: str) -> str:
    """
    Classify the topic of the prompt into a category for template selection.
    """
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["pizza","ice cream","burger","food","meal","snack","dish"]):
        return "food"
    elif any(word in prompt_lower for word in ["beach","soccer","game","playing","travel","vacation","hobby"]):
        return "activity"
    elif any(word in prompt_lower for word in ["dog","cat","pet","animal","bird","fish"]):
        return "animal"
    else:
        return "generic"

# -----------------------------
# Rule-based paragraph templates
# -----------------------------
TEMPLATES = {
    "food": {
        "positive": [
            "Pizza is absolutely delicious and loved by people of all ages.",
            "The combination of flavors and textures makes every bite enjoyable.",
            "It's the perfect comfort food for any occasion."
        ],
        "negative": [
            "While pizza can be tasty, overindulging may affect your health.",
            "Some people find it greasy or too heavy after a meal.",
            "It's best enjoyed occasionally rather than every day."
        ],
        "neutral": [
            "Pizza is a widely known dish made from dough, sauce, and cheese.",
            "It comes in various styles and is popular in many countries.",
            "People enjoy it in different ways depending on local preferences."
        ]
    },
    "activity": {
        "positive": [
            "Playing soccer is an exciting way to stay active and social.",
            "It brings energy and joy to participants of all ages.",
            "Friendly matches create great memories with friends and family."
        ],
        "negative": [
            "Soccer can be tiring and sometimes frustrating for beginners.",
            "Injuries may occur if players are not careful.",
            "Some people prefer less physically demanding activities."
        ],
        "neutral": [
            "Soccer is a sport played by two teams of eleven players.",
            "It is popular worldwide and has various professional leagues.",
            "People play it for exercise, competition, or leisure."
        ]
    },
    "animal": {
        "positive": [
            "Dogs are loyal companions known for their friendliness and energy.",
            "They bring warmth and happiness to many households.",
            "Spending time with a dog can brighten anyone's day."
        ],
        "negative": [
            "Owning a dog can be challenging due to time, cost, and training needs.",
            "Some dogs have behavioral issues that require patience.",
            "It’s important to consider responsibilities before adopting a pet."
        ],
        "neutral": [
            "Dogs are domesticated animals kept as pets in many homes.",
            "They come in various breeds, sizes, and temperaments.",
            "People care for them by providing food, shelter, and attention."
        ]
    },
    "generic": {
        "positive": [
            "This topic is widely appreciated for its positive impact.",
            "It often inspires enthusiasm and interest in many people.",
            "Engaging with it can bring joy and satisfaction."
        ],
        "negative": [
            "This topic has some drawbacks and challenges to consider.",
            "Critics point out potential issues that need attention.",
            "Caution and thoughtful engagement are advised."
        ],
        "neutral": [
            "This is a subject of ongoing discussion with varied perspectives.",
            "Different people have different opinions depending on context.",
            "It is widely studied and analyzed across fields."
        ]
    }
}

# -----------------------------
# Paragraph generation
# -----------------------------
def generate_rule_based_paragraph(prompt: str, sentiment: str) -> str:
    """
    Generate a paragraph based on topic type and sentiment.
    """
    topic_type = classify_topic_type(prompt)
    if topic_type not in TEMPLATES:
        topic_type = "generic"  # fallback

    sentences = TEMPLATES[topic_type].get(sentiment, TEMPLATES["generic"]["neutral"])
    random.shuffle(sentences)
    return " ".join(sentences)

# -----------------------------
# Main generator function
# -----------------------------
def generate_text(prompt: str, sentiment: str = None) -> str:
    """
    Generate a sentiment-aligned paragraph for the given prompt.
    If sentiment is None or 'auto', detect it using sentiment.py.
    """
    if sentiment is None or sentiment.lower() == "auto":
        sentiment = detect_sentiment(prompt)

    return generate_rule_based_paragraph(prompt, sentiment)
