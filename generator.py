import os
import random

# Try to import anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


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


def rewrite_prompt_for_claude(user_input, sentiment):
    """Reframe casual input into a natural, sentiment-aligned topic"""
    topic = extract_topic_keywords(user_input).capitalize()

    if sentiment == "positive":
        return f"{topic} is widely loved and appreciated. Here's a joyful reflection:"
    elif sentiment == "negative":
        return f"{topic} has sparked concern or criticism. Here's a critical perspective:"
    else:
        return f"{topic} is a topic of interest. Here's an objective summary:"


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
    """Improved rule-based generation that's more contextual"""
    topic = extract_topic_keywords(prompt)

    templates = {
        'positive': [
            f"{topic.capitalize()} is beloved by many for its positive impact and widespread appeal. It brings people together and continues to inspire enthusiasm across communities."
        ],
        'negative': [
            f"{topic.capitalize()} has raised concerns due to its potential drawbacks and ongoing challenges. Critics argue that it requires closer scrutiny and reform."
        ],
        'neutral': [
            f"{topic.capitalize()} is a subject of ongoing discussion. It presents a range of perspectives and outcomes depending on context and interpretation."
        ]
    }

    options = templates.get(sentiment, templates['neutral'])
    return random.choice(options)


def generate_text(prompt, sentiment, word_count=150):
    """
    Main generation function - tries API first, then improved rule-based fallback
    """
    print(f"generate_text called with: prompt='{prompt}', sentiment='{sentiment}'")  # Debug

    # Try API first
    text = generate_with_api(prompt, sentiment, word_count)
    if text:
        return text

    print("Falling back to rule-based generation")  # Debug
    return generate_rule_based(prompt, sentiment, word_count)
