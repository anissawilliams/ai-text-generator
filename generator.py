import os
import streamlit as st
import requests

# ----------------------------------------
# Hugging Face API setup
# ----------------------------------------
HF_API_TOKEN = st.secrets.get("HF_API_TOKEN") or os.environ.get("HF_API_TOKEN")
HF_MODEL = "mosaicml/mpt-7b-instruct"  # Instruction-tuned model

HAS_HF = True if HF_API_TOKEN else False
if not HAS_HF:
    st.warning("⚠️ No Hugging Face API key found. Using rule-based fallback.")


# ----------------------------------------
# Rule-based examples for fallback
# ----------------------------------------
FEW_SHOT_EXAMPLES = """## Examples
Positive: Ice cream is a delightful treat enjoyed by people of all ages.
Negative: Fast food has been criticized for its health impacts.
Neutral: Pasta is a staple food commonly served with sauces or vegetables.
"""


# ----------------------------------------
# Helper functions
# ----------------------------------------
def extract_topic_keywords(prompt: str) -> str:
    """Extract key topic words from the prompt."""
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
    return ' '.join(keywords[:5]) if keywords else prompt


def classify_topic_type(prompt: str) -> str:
    """Classify topic for rule-based fallback."""
    prompt = prompt.lower()
    if any(word in prompt for word in ["pizza","ice cream","burger","food","meal","snack","dish"]):
        return "food"
    elif any(word in prompt for word in ["beach","soccer","game","watching","playing","travel","vacation","hobby"]):
        return "activity"
    elif any(word in prompt for word in ["dog","cat","pet","animal","bird","fish"]):
        return "animal"
    else:
        return "generic"


# ----------------------------------------
# Hugging Face generation
# ----------------------------------------
def generate_with_hf(prompt: str, sentiment: str, word_count: int = 150) -> str | None:
    """Generate text using Hugging Face Inference API."""
    if not HAS_HF:
        return None

    topic = extract_topic_keywords(prompt).capitalize()
    hf_prompt = f"Write a {sentiment} paragraph about {topic} in a friendly, casual tone. Around {word_count} words."

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": hf_prompt}

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        # Hugging Face outputs text under 'generated_text'
        text = data[0]["generated_text"].strip()
        return text
    except Exception as e:
        st.error(f"❌ HF generation failed: {type(e).__name__}: {e}")
        return None


# ----------------------------------------
# Rule-based fallback
# ----------------------------------------
def generate_rule_based(prompt: str, sentiment: str, word_count: int = 150) -> str:
    topic = extract_topic_keywords(prompt).capitalize()
    topic_type = classify_topic_type(prompt)
    templates = {
        "food": {
            "positive": f"{topic} is absolutely delicious and loved by people of all ages.",
            "negative": f"While many enjoy {topic}, some find it unhealthy or overly indulgent.",
            "neutral": f"{topic} is a type of food commonly enjoyed in various cultures."
        },
        "activity": {
            "positive": f"{topic} is a fun and relaxing way to spend time.",
            "negative": f"Some people find {topic} exhausting or unappealing.",
            "neutral": f"{topic} is a common activity enjoyed by people for leisure."
        },
        "animal": {
            "positive": f"{topic} is a beloved companion known for its loyalty and charm.",
            "negative": f"{topic} ownership can be challenging due to time, cost, and behavioral issues.",
            "neutral": f"{topic} is a domesticated animal found in many homes."
        },
        "generic": {
            "positive": f"{topic} is widely appreciated for its positive impact and appeal.",
            "negative": f"{topic} has drawbacks and challenges to consider.",
            "neutral": f"{topic} is a
