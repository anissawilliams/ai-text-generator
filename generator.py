import os
import random

# Try to import anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Canonical few-shot examples for casual tone
FEW_SHOT_EXAMPLES = """## Examples
Positive: Ice cream is a delightful treat enjoyed by people of all ages, especially during warm weather.
Negative: Fast food has been criticized for its health impacts and contribution to poor dietary habits.
Neutral: Pasta is a staple food made from wheat and water, commonly served with sauces or vegetables.

Positive: Playing video games can be a fun and relaxing way to unwind after a long day.
Negative: Spending too much time on social media can lead to stress, distraction, and reduced productivity.
Neutral: Board games are tabletop games that involve counters or pieces moved on a pre-marked surface.

Positive: Dogs are loyal companions that bring joy, comfort, and energy to their owners.
Negative: Owning a pet can be challenging due to time commitments, expenses, and behavioral issues.
Neutral: Cats are domesticated animals known for their independence and quiet nature.
"""

def extract_topic_keywords(prompt):
    """Extract key topic words from the prompt"""
    stop_words = {
        'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'it', 'they',
        'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did',
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because',
        'as', 'what', 'which', 'this', 'that', 'these', 'those',
        'love', 'hate', 'like', 'think', 'feel', 'believe',
        'how', 'why', 'when', 'where', 'who'
    }

    words = prompt.lower().split()
    keywords = [w.strip('.,!?;:') for w in words if w.strip('.,!?;:') not in stop_words]
    return ' '.join(keywords[:5]) if keywords else prompt

def classify_topic_type(prompt):
    """Classify topic into a basic type"""
    prompt = prompt.lower()
    if any(word in prompt for word in ["pizza", "ice cream", "burger", "food", "meal", "snack", "dish"]):
        return "food"
    elif any(word in prompt for word in ["beach", "soccer", "game", "watching", "playing", "travel", "vacation", "hobby"]):
        return "activity"
    elif any(word in prompt for word in ["dog", "cat", "pet", "animal", "bird", "fish"]):
        return "animal"
    else:
        return "generic"

def rewrite_prompt_for_claude(user_input, sentiment):
    """Reframe input into a concise and effective prompt."""
    topic = extract_topic_keywords(user_input).capitalize()
    sentiment = sentiment.lower()

    return f"""Write one short paragraph (60–90 words) expressing a {sentiment} sentiment about "{topic}". 
Use a natural, conversational tone — like something you'd say in casual writing. 
Do not include headings, lists, or markdown formatting. 
Focus on vivid but simple language.
"""

def generate_with_api(prompt, sentiment, word_count):
    """Generate using Claude API (improved)."""
    if not HAS_ANTHROPIC:
        print("Anthropic library not available")
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key found in environment")
        return None

    try:
        client = anthropic.Anthropic(api_key=api_key)
        rewritten_prompt = rewrite_prompt_for_claude(prompt, sentiment)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # newer stable version
            max_tokens=300,
            temperature=0.8,  # Add variety and tone warmth
            messages=[{"role": "user", "content": rewritten_prompt}]
        )

        text = message.content[0].text.strip()

        # Clean any markdown or extra formatting Claude adds
        text = text.replace("**", "").replace("#", "").strip()

        # Optional: truncate to roughly the desired length
        words = text.split()
        if len(words) > word_count:
            text = " ".join(words[:word_count]) + "..."

        return text

    except Exception as e:
        print(f"API generation failed: {e}")
        return None


def generate_rule_based(prompt, sentiment, word_count):
    """Rule-based fallback with contextual phrasing"""
    topic = extract_topic_keywords(prompt).capitalize()
    topic_type = classify_topic_type(prompt)

    templates = {
        "food": {
            "positive": f"{topic} is absolutely delicious and loved by people of all ages. It's a go-to comfort food that never disappoints.",
            "negative": f"While many enjoy {topic}, some find it unhealthy or overly indulgent. It's best in moderation.",
            "neutral": f"{topic} is a type of food commonly enjoyed in various cultures and settings."
        },
        "activity": {
            "positive": f"{topic} is a fun and relaxing way to spend time. It brings joy, energy, and great memories.",
            "negative": f"Some people find {topic} exhausting or unappealing, especially when it's overdone or poorly organized.",
            "neutral": f"{topic} is a common activity enjoyed by people for entertainment, exercise, or leisure."
        },
        "animal": {
            "positive": f"{topic} is a beloved companion known for its loyalty and charm. It brings warmth to many households.",
            "negative": f"{topic} ownership can be challenging due to time, cost, and behavioral issues.",
            "neutral": f"{topic} is a domesticated animal found in many homes around the world."
        },
        "generic": {
            "positive": f"{topic} is widely appreciated for its positive impact and appeal. It continues to inspire enthusiasm.",
            "negative": f"{topic} has raised concerns due to its drawbacks and challenges. Critics urge caution and reform.",
            "neutral": f"{topic} is a subject of ongoing discussion with varied perspectives depending on context."
        }
    }

    return templates[topic_type][sentiment]

def generate_text(prompt, sentiment, word_count=150):
    """Main generation function - tries API first, then rule-based fallback"""
    print(f"generate_text called with: prompt='{prompt}', sentiment='{sentiment}'")  # Debug

    text = generate_with_api(prompt, sentiment, word_count)
    if text:
        return text

    print("Falling back to rule-based generation")  # Debug
    return generate_rule_based(prompt, sentiment, word_count)
