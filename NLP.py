#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from textblob import TextBlob
import syllables

# Download necessary NLTK corpora
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Read the URLs from the Excel file
data = pd.read_excel(r'C:\Users\ADMIN\Downloads\Input.xlsx', names=['URL_ID', 'URL'])

# Create an empty DataFrame to store the output variables
output = pd.DataFrame(columns=['URL_ID', 'URL', 'positive_score', 'negative_score', 'polarity_score', 'subjectivity_score', 'avg_sentence_length', 'percent_complex_words', 'fog_index', 'avg_words_per_sentence', 'complex_word_count', 'word_count', 'syllables_per_word', 'personal_pronouns', 'avg_word_length'])

# Loop through each URL in the DataFrame and extract the output variables
url_id_index = data.columns.get_loc('URL_ID')
url_index = data.columns.get_loc('URL')

for row in data.itertuples(index=False):
    url_id = row[url_id_index]
    url = row[url_index]

    # process the URL here
    try:
        response = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
        if response.status_code == 200:
            print("URL is valid and accessible.")
        else:
            print("URL is valid, but cannot be accessed.")
            continue
    except requests.exceptions.InvalidURL:
        print("Invalid URL")
        continue
    except requests.exceptions.ConnectionError:
        print("Cannot connect to URL")
        continue

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the text content from the HTML
    text = soup.get_text()

    # Tokenize the text into sentences and words
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)

    # Compute the number of words and complex words
    word_count = len(words)
    complex_word_count = len([word for word in words if len(word) > 2 and nltk.pos_tag([word])[0][1] in ['JJ', 'VB', 'VBN', 'VBG']])

    # Compute the average number of words per sentence and percentage of complex words
    avg_words_per_sentence = word_count / len(sentences)
    percent_complex_words = complex_word_count / word_count * 100
# Compute the FOG index
    fog_index = 0.4 * (avg_words_per_sentence + percent_complex_words)

    # Compute the syllables per word
    syllables_per_word = sum(syllables.estimate(word) for word in words) / word_count

    # Compute the personal pronouns count
    personal_pronouns = len([word for word in words if nltk.pos_tag([word])[0][1] == 'PRP'])

    # Compute the average word length
    avg_word_length = sum(len(word) for word in words) / word_count

    # Compute the polarity and subjectivity scores using TextBlob
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity

    # Compute the positive and negative scores
    positive_score = sum(1 for sentence in sentences if TextBlob(sentence).sentiment.polarity > 0) / len(sentences)
    negative_score = sum(1 for sentence in sentences if TextBlob(sentence).sentiment.polarity < 0) / len(sentences)

    # Add the output variables to the DataFrame
    output = output.append({'URL': url, 'positive_score': positive_score, 'negative_score': negative_score, 'polarity_score': polarity_score, 'subjectivity_score': subjectivity_score, 'avg_sentence_length': avg_words_per_sentence, 'percent_complex_words': percent_complex_words, 'fog_index': fog_index, 'avg_words_per_sentence': avg_words_per_sentence, 'complex_word_count': complex_word_count, 'word_count': word_count,'syllables_per_word':syllables_per_word,'personal_pronouns': personal_pronouns,'avg_word_length': avg_word_length},ignore_index=True)
    # Save the output DataFrame to an Excel file
output.to_excel('output.xlsx', index=False)
from IPython.display import FileLink
display(FileLink('output.xlsx'))


# In[2]:


pip install syllables


# In[ ]:




