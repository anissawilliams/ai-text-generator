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
