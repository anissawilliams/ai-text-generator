import os
import streamlit as st
from huggingface_hub import InferenceClient

# -----------------------------
# Hugging Face API setup
# -----------------------------
HF_TOKEN = st.secrets.get("HF_API_TOKEN") or os.environ.get("HF_API_TOKEN")
if not HF_TOKEN:
    st.warning("⚠️ No Hugging Face API token found; will use rule-based fallback.")
HAS_HF = bool(HF_TOKEN)

# Pick a model that works with free inference
HF_MODEL = "tiiuae/falcon-7b-instruct"

if HAS_HF:
    hf_client = InferenceClient(api_key=HF_TOKEN)

# -----------------------------
# Helper functions
# -----------------------------
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
    return ' '.join(keywords[:5]) if keywords else prompt

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

# -----------------------------
# Hugging Face generation
# -----------------------------
def generate_with_hf(prompt: str, sentiment: str, word_count: int = 150) -> str | None:
    if not HAS_HF:
        return None

    topic = extract_topic_keywords(prompt).capitalize()
    hf_prompt = (f"Write a {sentiment} paragraph about {topic} "
                 f"in a friendly, casual tone, around {word_count} words.")

    try:
        # Correct positional usage of text_generation
        resp = hf_client.text_generation(
            hf_prompt,  # prompt as positional argument
            model=HF_MODEL,
            parameters={"max_new_tokens": word_count, "temperature": 0.8}
        )
        # Extract generated text
        text = resp[0]["generated_text"] if isinstance(resp, list) else resp["generated_text"]
        return text.strip()
    except Exception as e:
        st.error(f"❌ HF generation failed: {type(e).__name__}: {e}")
        return None

# -----------------------------
# Rule-based fallback
# -----------------------------
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
            "neutral": f"{topic} is a subject of ongoing discussion."
        }
    }
    return templates[topic_type].get(sentiment, templates["generic"]["neutral"])

# -----------------------------
# Main generation function
# -----------------------------
def generate_text(prompt: str, sentiment: str, word_count: int = 150) -> str:
    st.info(f"Generating text for topic='{prompt}' with sentiment='{sentiment}'...")
    text = generate_with_hf(prompt, sentiment, word_count)
    if text:
        return text
    st.warning("Falling back to rule-based generation.")
    return generate_rule_based(prompt, sentiment, word_count)
