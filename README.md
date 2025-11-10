## How to run
pip install streamlit
pip install transformers

In a terminal window, streamlit run app.py. A local server will be started.
I have deployed it on Streamlit Cloud. You'll just have to navigate to  https://ai-text-gener8r.streamlit.app
and wake it up.

## Technologies Used
streamlit - for the UI (I've used this before and it's easy to use)
transformers - for the sentiment analysis model. This worked well and was consistent. 
anthropic - for the text generation model. As mentioned below, I switched gears and moved to this from huggingface text generation(gpt2-medium, several others)

### Files 
app.py - the main file
generator.py - the text generation code
sentiment.py - the sentiment analysis code
requirements.txt - the list of dependencies needed for the app to run in Streamlit Cloud

## Challenges Encountered

I wanted to use a tried and true library for this (huggingface). The text generation often was taking too long and was way too wordy. I tweaked it using max_length and truncation. I also had to extract the topic from the sentimenta and provide several examples of output. I continued to get poor results even when I changed models and gave more information. I switched gears and moved from huggingface to Anthropic. Note - at this point I did have some help from Claude.ai to help me refactor with the new model. The results were much better and I further tweaked the generator code to get rid of the extra words that I didn't want to pass as the topic. 

## Future Improvements

More modern styling.