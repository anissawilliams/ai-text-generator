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
                f"Communities worldwide are already experiencing the positive impacts, with measurable improvements in quality of life and opportunity.",
                f"The collaborative efforts driving this forward demonstrate the power of collective action and shared vision.",
            ],
            'conclusion': [
                f"Looking ahead, {prompt} promises to continue reshaping our world in profoundly beneficial ways.",
                f"With continued investment and thoughtful implementation, the future of {prompt} appears exceptionally bright.",
                f"As we embrace these changes, the possibilities for positive impact seem limitless.",
            ]
        },
        'negative': {
            'intro': [
                f"The rise of {prompt} has sparked serious concerns among experts and communities alike.",
                f"When analyzing {prompt}, troubling patterns emerge that cannot be ignored.",
                f"The proliferation of {prompt} presents significant challenges that threaten established systems.",
                f"Critics warn that {prompt} may cause more harm than good if left unchecked.",
            ],
            'body': [
                f"Key issues include widening inequality, erosion of traditional safeguards, and unintended negative consequences.",
                f"Research indicates that vulnerable populations face disproportionate risks, exacerbating existing disparities.",
                f"The rapid pace of change has outstripped our ability to implement adequate protections and oversight.",
                f"Economic pressures and competing interests often prioritize short-term gains over long-term sustainability.",
            ],
            'conclusion': [
                f"Without immediate action, the problems associated with {prompt} will only intensify.",
                f"The costs of inaction far outweigh the challenges of implementing necessary reforms.",
                f"Until these fundamental issues are addressed, {prompt} remains a source of justified concern.",
            ]
        },
        'neutral': {
            'intro': [
                f"The topic of {prompt} has garnered significant attention from researchers and policymakers.",
                f"Understanding {prompt} requires careful examination of multiple perspectives and available data.",
                f"Recent studies on {prompt} have produced mixed findings that warrant further investigation.",
                f"{prompt} represents a complex phenomenon with both supporters and critics.",
            ],
            'body': [
                f"Evidence suggests that outcomes vary considerably depending on context, implementation, and demographic factors.",
                f"Proponents highlight potential benefits while skeptics raise legitimate questions about risks and tradeoffs.",
                f"The data shows both positive and negative trends across different regions and populations.",
                f"Experts emphasize the need for balanced approaches that consider diverse stakeholder interests.",
            ],
            'conclusion': [
                f"Further research is needed to fully understand the implications of {prompt}.",
                f"Policymakers face difficult choices as they navigate competing priorities and limited resources.",
                f"The debate surrounding {prompt} continues to evolve as new information emerges.",
            ]
        }
    }

    # Select appropriate templates
    sentiment_templates = templates.get(sentiment, templates['neutral'])

    # Build paragraph
    intro = random.choice(sentiment_templates['intro'])
    body = random.choice(sentiment_templates['body'])
    conclusion = random.choice(sentiment_templates['conclusion'])

    paragraph = f"{intro} {body} {conclusion}"

    return paragraph


def generate_text(prompt, sentiment, word_count=150):
    """
    Main generation function - tries API first, then rule-based fallback
    """
    # Try API first
    text = generate_with_api(prompt, sentiment, word_count)
    if text:
        return text

    # Fallback to rule-based generation
    return generate_rule_based(prompt, sentiment, word_count)