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
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

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

        return message.content[0].text

    except Exception as e:
        print(f"API generation failed: {e}")
        return None


def generate_rule_based(prompt, sentiment, word_count):
    """Enhanced rule-based generation when API is unavailable"""

    templates = {
        'positive': {
            'intro': [
                f"The emergence of {prompt} represents a significant breakthrough in modern society.",
                f"When examining {prompt}, we discover remarkable opportunities for positive transformation.",
                f"The advancement of {prompt} has opened exciting new pathways for innovation and growth.",
                f"{prompt} stands as a testament to human ingenuity and our capacity for progress.",
            ],
            'body': [
                f"This development brings numerous benefits, including enhanced efficiency, improved accessibility, and greater inclusivity.",
                f"Experts agree that the potential applications are vast, touching everything from education to healthcare to environmental sustainability.",
                f"Communities worldwide are already experiencing the positive impacts, with measurable improvements in quality of