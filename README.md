# Sentiment-Aligned Text Generation

An AI-powered application that generates paragraphs based on the sentiment of user prompts. The system automatically detects sentiment (positive, negative, neutral) and produces contextually appropriate text using Claude AI.

## Features

- **Automatic Sentiment Detection**: Analyzes input prompts to determine emotional tone using Hugging Face's Sentiment Analysis model
- **AI-Powered Generation**: Uses Claude Sonnet 4.5 for high-quality, coherent paragraph generation
- **Interactive Web Interface**: Built with Streamlit for seamless user experience
- **Sentiment-Aligned Output**: Generates text that matches the detected or selected sentiment

## Technology Stack

- **Python 3.x**
- **Anthropic Claude API** (Sonnet 4.5) - Text generation
- **Streamlit** - Frontend framework
- **Custom Sentiment Analysis** - Prompt classification

## Setup Instructions

Note: This project is available at https://ai-text-gener8r.streamlit.app
### Prerequisites
- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/settings/keys))
- API credits in your Anthropic account

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/anissawilliams/ai-text-generator
cd ai-text-generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API credentials**

Create `.streamlit/secrets.toml` in your project directory:
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-key-here"
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure
```
.
├── app.py                 # Main Streamlit application
├── sentiment.py           # Sentiment detection module
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # API key configuration (not committed)
└── README.md             # Project documentation
```

## How It Works

1. **User Input**: User enters a text prompt in the web interface
2. **Sentiment Detection**: The `sentiment.py` module analyzes the prompt to determine its sentiment (positive, negative, or neutral)
3. **Text Generation**: Claude Sonnet 4.5 generates a 4-6 sentence paragraph matching the detected sentiment
4. **Output Display**: The generated text is displayed to the user

### Technical Approach

**Sentiment Analysis**:
- Custom implementation in `sentiment.py`
- Classifies prompts into positive, negative, or neutral categories
- Provides sentiment context to the generation model

**Text Generation**:
- Uses Anthropic's Claude Sonnet 4.5 model
- System prompt engineering to align output with detected sentiment
- Temperature setting (0.7) for creative yet coherent responses
- Max tokens: 500 for complete paragraph generation

**Frontend**:
- Streamlit provides rapid prototyping and clean UI (and I have experience with it!)
- Real-time interaction between user input and AI output
- Simple deployment process

## Requirements
```txt
streamlit
anthropic
transformers
torch
tokenizers
```

## Usage Example

1. Enter a prompt: *"Tell me about a beautiful sunset"*
2. System detects: **Positive sentiment**
3. Generated output: A vivid, uplifting paragraph about sunsets with warm, optimistic language

## Challenges & Solutions

**Challenge 1: Text Generation Quality**
- *Issue*: Initial use of Hugging Face's text generation model provided poor results despite proper prompt engineering
- *Solution*: Upgraded to Claude Sonnet 4.5 with enhanced prompt engineering

**Challenge 2: API Authentication**
- *Issue*: Credit balance requirements for API access
- *Solution*: Added credits to Anthropic account; implemented proper error handling

**Challenge 3: Sentiment Alignment**
- *Issue*: Ensuring generated text truly matches detected sentiment
- *Solution*: Detailed system prompts with specific tone instructions and style guidelines

## Optional Enhancements

- [ ] Manual sentiment selection override
- [ ] Adjustable output length (paragraph vs. essay)
- [ ] Multiple paragraph generation
- [ ] Sentiment confidence scores
- [ ] Export generated text functionality

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `ANTHROPIC_API_KEY` in app settings under "Secrets"
5. Deploy!

**Note**: Ensure you have API credits in your Anthropic account before deployment.

## Cost Considerations

- Claude Sonnet 4.5 pricing: ~$3 per million input tokens, ~$15 per million output tokens
- Typical generation (~500 tokens) costs less than $0.01
- Minimum API credit purchase: $5 (sufficient for extensive testing)

## License

[Your License Here]

## Author

[Your Name]

## Acknowledgments

- Anthropic for Claude AI API
- Streamlit for the web framework