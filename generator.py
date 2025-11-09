import os
import random

# Try to import anthropic
try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


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

        sentiment_guides = {
            'positive': 'optimistic, hopeful, and enthusiastic tone. Highlight benefits, opportunities, and positive aspects.',
            'negative': 'critical, pessimistic, or concerning tone. Focus on problems, challenges, and drawbacks.',
            'neutral': 'balanced, objective, and factual tone. Present information without emotional bias.'
        }

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Write a {sentiment} paragraph about: "{prompt}"

Requirements:
- Use a {sentiment_guides[sentiment]}
- Write approximately {word_count} words
- Make it coherent, well-structured, and natural
- Match the {sentiment} sentiment consistently throughout

Write the paragraph now:"""
            }]
        )

        print("API call successful!")  # Debug
        return message.content[0].text

    except Exception as e:
        print(f"API generation failed with error: {type(e).__name__}: {str(e)}")
        return None


def extract_topic_keywords(prompt):
    """Extract key topic words from the prompt"""
    stop_words = {'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'it', 'they',
                  'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did',
                  'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because',
                  'as', 'what', 'which', 'this', 'that', 'these', 'those',
                  'love', 'hate', 'like', 'think', 'feel', 'believe',
                  'how', 'why', 'when', 'where', 'who'}

    words = prompt.lower().split()
    keywords = [w.strip('.,!?;:') for w in words if w.strip('.,!?;:') not in stop_words]

    return ' '.join(keywords[:5]) if keywords else prompt


def generate_rule_based(prompt, sentiment, word_count):
    """Improved rule-based generation that's more contextual"""

    topic = extract_topic_keywords(prompt)

    templates = {
        'positive': [
            f"The subject of {topic} brings remarkable opportunities and positive developments to our society. This area has shown tremendous growth and innovation, with communities experiencing tangible benefits and improved outcomes. Experts highlight the transformative potential, noting how {topic} creates pathways for progress and empowerment. The enthusiasm surrounding this topic is well-founded, as evidence demonstrates meaningful positive impacts across diverse populations. Looking forward, the continued advancement of {topic} promises even greater benefits, fostering hope and optimism for the future.",
        ],
        'negative': [
            f"The issue of {topic} raises serious concerns that demand immediate attention and critical examination. Evidence suggests troubling patterns emerging, with negative consequences affecting vulnerable populations disproportionately. Experts warn about the risks associated with {topic}, pointing to systemic problems and inadequate safeguards. The current trajectory appears unsustainable, threatening to exacerbate existing inequalities and create new challenges. Without significant intervention and reform, the problems surrounding {topic} will likely intensify, causing further harm and destabilization.",
        ],
        'neutral': [
            f"The topic of {topic} presents a complex landscape that merits careful, balanced examination from multiple perspectives. Research in this area reveals mixed findings, with outcomes varying significantly based on context, implementation approaches, and demographic factors. Stakeholders hold divergent views about {topic}, with valid arguments on different sides of key debates. Data shows both positive and negative trends across various metrics, suggesting that simplistic conclusions would be premature. Continued study and evidence-gathering remain essential for developing nuanced understanding of {topic}.",
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
    # Fallback to improved rule-based generation
    return generate_rule_based(prompt, sentiment, word_count)