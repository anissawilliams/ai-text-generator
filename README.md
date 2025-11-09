## How to run
pip install streamlit
pip install transformers

In a terminal window, streamlit run app.py. A local server will be started.
I have deployed it on Streamlit Cloud. You'll just have to navigate to the link and wake it up.



## Challenges Encountered

I wanted to use a tried and true library for this. I used huggingface but it often was taking too long and also way too wordy. I tweaked it using max_length and truncation. I also had to extract the topic from the sentiment.

## Future Improvements

Slider to determine the length of the response.
More modern styling.