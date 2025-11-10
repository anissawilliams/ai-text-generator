import os
import random

# Try to import anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Few-shot examples to guide Claude's tone and structure
FEW_SHOT_EXAMPLES = """Examples:
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

def is_casual_topic(prompt):
    """Detect if the topic is casual/personal"""
    casual_keywords = ["food", "movie", "music", "holiday", "game", "hobby", "favorite", "love", "like", "enjoy", "watching", "playing"]
    return any(word in prompt.lower() for word in casual_keywords)

def rewrite_prompt_for_claude(user_input, sentiment):
    """Reframe input with few-shot examples and tone guidance"""
    topic = extract_topic_keywords(user_input).capitalize()
    tone = "friendly and natural tone for a casual audience"

    return f"""{FEW_SHOT_EXAMPLES}

Now write a {sentiment} paragraph about {topic}, using a {tone}:"""

def generate_with_api(prompt, sentiment, word_count):
    """Generate using Claude API"""
    if not HAS_ANTHROPIC:
        print("Anthropic library not available")
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key found in environment")
        return None

    print(f"Attempting API call with key: {api_key[:10]}...")  # Debug

    try:
        client = anthropic.Anthropic(api_key=api_key)
        rewritten_prompt = rewrite_prompt_for_claude(prompt, sentiment)

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": rewritten_prompt
            }]
        )

        print("API call successful!")  # Debug
        return message.content[0].text

    except Exception as e:
        print(f"API generation failed with error: {type(e).__name__}: {str(e)}")
        return None

def generate_rule_based(prompt, sentiment, word_count):
    """Rule-based fallback with casual tone support"""
    topic = extract_topic_keywords(prompt)
    casual = is_casual_topic(prompt)

    if casual:
        templates = {
            'positive': [
                f"{topic.capitalize()} is a fun and enjoyable part of everyday life. It brings people together and always adds a little joy."
            ],
            'negative': [
                f"While many enjoy {topic}, some find it overwhelming or distracting. It's best enjoyed in moderation."
            ],
            'neutral': [
                f"{topic.capitalize()} is a common activity that people engage in for entertainment or relaxation."
            ]
        }
    else:
        templates = {
            'positive': [
                f"{topic.capitalize()} is widely appreciated for its benefits and positive impact. It continues to inspire enthusiasm and innovation."
            ],
            'negative': [
                f"{topic.capitalize()} has raised concerns due to its drawbacks and ongoing challenges. Critics argue that it requires closer scrutiny and reform."
            ],
            'neutral': [
                f"{topic.capitalize()} is a subject of ongoing discussion. It presents a range of perspectives depending on context and interpretation."
            ]
        }

    options = templates.get(sentiment, templates['neutral'])
    return random.choice(options)

def generate_text(prompt, sentiment, word_count=150):
    """Main generation function - tries API first, then rule-based fallback"""
    print(f"generate_text called with: prompt='{prompt}', sentiment='{sentiment}'")  # Debug

    text = generate_with_api(prompt, sentiment, word_count)
    if text:
        return text

    print("Falling back to rule-based generation")  # Debug
    return generate_rule_based(prompt, sentiment, word_count)
