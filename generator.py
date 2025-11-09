import anthropic
import os


# Alternative: Using local models if you don't want API
def generate_text_with_api(prompt, sentiment, word_count=150):
    """
    Generate text using Claude API (requires ANTHROPIC_API_KEY env variable)
    """
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    sentiment_guides = {
        'positive': 'optimistic, hopeful, and enthusiastic tone. Highlight benefits, opportunities, and positive aspects.',
        'negative': 'critical, pessimistic, or concerning tone. Focus on problems, challenges, and drawbacks.',
        'neutral': 'balanced, objective, and factual tone. Present information without emotional bias.'
    }

    system_prompt = f"""Write a {sentiment} paragraph about the given topic.

Requirements:
- Use a {sentiment_guides[sentiment]}
- Write approximately {word_count} words
- Make it coherent, well-structured, and natural
- Match the {sentiment} sentiment consistently throughout"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Topic: {prompt}\n\nWrite the paragraph now:"}
        ],
        system=system_prompt
    )

    return message.content[0].text


def generate_text_with_gpt2(prompt, sentiment, word_count=150):
    """
    Generate text using local GPT-2 model (no API needed)
    Much better prompting strategy than your original
    """
    from transformers import pipeline, set_seed
    set_seed(42)

    generator = pipeline('text-generation', model='gpt2-medium')  # Using medium for better quality

    # Few-shot examples for each sentiment
    examples = {
        'positive': [
            "Renewable energy has revolutionized our approach to sustainability, offering clean alternatives that reduce carbon emissions and create green jobs.",
            "The community's collaborative spirit has fostered innovation, bringing people together to solve problems and celebrate achievements."
        ],
        'negative': [
            "Rising inequality continues to widen the gap between rich and poor, creating systemic barriers that limit opportunities for millions.",
            "Environmental degradation accelerates unchecked, threatening ecosystems and future generations with irreversible damage."
        ],
        'neutral': [
            "The policy was implemented in 2023, affecting approximately 2 million individuals across various demographics and regions.",
            "Research indicates that the phenomenon occurs under specific conditions, with measurable effects documented in controlled studies."
        ]
    }

    # Build enhanced prompt
    example_text = "\n".join(examples[sentiment])
    full_prompt = f"""Below are examples of {sentiment} writing:

{example_text}

Now write a {sentiment} paragraph about: {prompt}

"""

    # Generate with better parameters
    result = generator(
        full_prompt,
        max_length=len(full_prompt.split()) + word_count,
        num_return_sequences=1,
        temperature=0.8,
        top_p=0.92,
        repetition_penalty=1.3,
        do_sample=True,
        pad_token_id=50256
    )

    # Extract only the generated part (remove prompt)
    generated = result[0]['generated_text']
    generated = generated[len(full_prompt):].strip()

    return generated


# Main function that you'll call
def generate_text(prompt, sentiment, word_count=150):
    """
    Main generation function. 
    Uses API if available, falls back to GPT-2
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return generate_text_with_api(prompt, sentiment, word_count)
        except:
            print("API failed, falling back to local model...")

    return generate_text_with_gpt2(prompt, sentiment, word_count)