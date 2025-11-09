import os
from transformers import pipeline, set_seed
import warnings

warnings.filterwarnings('ignore')

# Try to import anthropic, but don't fail if not available
try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Lazy load GPT-2 to save memory
gpt2_generator = None


def get_gpt2_generator():
    """Lazy load GPT-2 generator"""
    global gpt2_generator
    if gpt2_generator is None:
        set_seed(42)
        gpt2_generator = pipeline('text-generation', model='gpt2')
    return gpt2_generator


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


def generate_with_gpt2(prompt, sentiment, word_count):
    """Generate using local GPT-2"""
    generator = get_gpt2_generator()

    # Sentiment-specific examples
    examples = {
        'positive': "Technology has transformed education, making learning accessible to millions worldwide and empowering students with unprecedented opportunities.",
        'negative': "Technology has disrupted traditional learning, creating digital divides and reducing meaningful human interaction in classrooms.",
        'neutral': "Technology has changed education through online platforms, digital resources, and remote learning capabilities."
    }

    # Build prompt
    full_prompt = f"""Example of {sentiment} writing:
{examples[sentiment]}

Write a {sentiment} paragraph about: {prompt}

Paragraph:"""

    # Generate
    result = generator(
        full_prompt,
        max_length=len(full_prompt.split()) + word_count + 20,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.5,
        do_sample=True,
        pad_token_id=50256
    )

    # Extract generated text (remove prompt)
    generated = result[0]['generated_text']
    generated = generated.split("Paragraph:")[-1].strip()

    # Clean up if it's too short or has issues
    if len(generated.split()) < 20:
        generated = f"The topic of {prompt} is significant in today's world. " + generated

    return generated


def generate_text(prompt, sentiment, word_count=150):
    """
    Main generation function with fallback logic
    """
    # Try API first
    text = generate_with_api(prompt, sentiment, word_count)
    if text:
        return text

    # Fallback to GPT-2
    return generate_with_gpt2(prompt, sentiment, word_count)