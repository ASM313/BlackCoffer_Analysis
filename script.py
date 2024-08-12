# Import neccessary stuff
import os
import nltk
nltk.download('punkt_tab')
from nltk import word_tokenize, sent_tokenize
import string
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests


"""
>>>>>>>>>>>>> Crawl the Article from web <<<<<<<<<<<<<<<<
"""

def crawl_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.text
    paragraphs = soup.find_all('p')
    article_text = ' '.join([para.text for para in paragraphs])

    ## All the articles have same content after wors "Summarized"

    position = article_text.find("Summarized")

    if position != -1:
        article_text=article_text[:position + len("Summarized")]

    return title + "\n" + article_text

"""
>>>>>>>>>>> Store all the stop words in a list<<<<<<<<<<<<<<<<<<<
"""


# Stopwords are given by client, files stored in "Stopwords" folder 

given_stop_words=[]

for item in os.listdir("StopWords"):
    f=open(f"StopWords/{item}", "r")
    for line in f:
        given_stop_words.append((line.split()[0]).lower())

        
"""
Defining a method for removing stopwords from article. 
"""
def remove_stopwords(article_text, given_stop_words):
    
    msg = article_text.lower()

    msg=word_tokenize(msg)
    filtered_words=[]
    
    for word in msg:
        if word not in given_stop_words:
            filtered_words.append(word)
            
    
    return filtered_words

"""
    Positive and Negative words are given, 
    So load them in lists:  positive_words and negative_words

"""
positive_words=[]
negative_words=[]

f = open("positive.txt", "r")
for line in f:
    positive_words.append((line.split()[0]).lower())    

print(f"Total Positive words are: {len(positive_words)}")    

f = open("negative.txt", "r")
for line in f:
    negative_words.append((line.split()[0]).lower())    

print(f"Total Negative words are: {len(negative_words)}")   

'''
    Creating a dictionary of Positive and Negative words 
    excluding `stopwords`
'''    

for word in positive_words:
    if word in given_stop_words:
        positive_words.pop(positive_words.index(word))

for word in negative_words:
    if word in given_stop_words:
        negative_words.pop(negative_words.index(word))

"""
    - Extracting Derived variables
    > i. Positive Score
    > ii. Negative Score
    > iii. Polarity Score
    > iv. Subjectivity Score 

"""


# Positive Score
def check_positive_score(filtered_words, positive_words):
    positive_score=0
    
    for word in filtered_words:
        if word in positive_words:
            positive_score+=1
    
    return positive_score

# Negative Score
def check_negative_score(filtered_words, negative_words):
    negative_score=0
    for word in filtered_words:
        if word in negative_words:
            negative_score-=1
    
    return negative_score*(-1)


# Polarity Score
def check_polarity_score(positive_score, negative_score):
    
    polarity_score = (positive_score-negative_score)/((positive_score+negative_score)+0.000001)
    
    return polarity_score


# Subjective Score
def check_subjective_score(filtered_words, positive_score, negative_score):
    
    subjective_score = (positive_score+negative_score)/(len(filtered_words)+0.000001)
    
    return subjective_score

"""
    Analysis of Readability
    
    > v. Average Sentence Length = the number of words / the number of sentences

    > vi. Percentage of Complex words = the number of complex words / the number of words 

    > vii. Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
"""

# Average Sentence Length
def compute_avg_sentence_length(article_text)-> float:
    total_words=len(word_tokenize(article_text))
    total_sentences=len(sent_tokenize(article_text))
    avg_length = total_words/total_sentences 
    return avg_length 


# Percentage of complex words
    """
    pronounce (a word or phrase) clearly, is called syllable.
    """
def syllable_count(word):
    vowels = "aeiou"
    word = word.lower()
    syllables = 0
    if word[0] in vowels:
        syllables += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllables += 1
    if word.endswith("es") or word.endswith("ed"):
        syllables -= 1
    if syllables == 0:
        syllables += 1
    return syllables

def complex_word_count(text)-> int:
    words = word_tokenize(text)
    complex_words = [word for word in words if syllable_count(word) > 2]
    return len(complex_words)

def percentage_of_complex_words(article_text) -> float:
    percentage = complex_word_count(article_text)/len(word_tokenize(article_text)) 
    return percentage


# Fog Index
def fog_index(article_text):
    avg_sentence = percent_of_complex_words = 0.0
    avg_sentence = compute_avg_sentence_length(article_text=article_content)
    percent_of_complex = percentage_of_complex_words(article_text=article_content)
    
    fg = (avg_sentence + percent_of_complex)
    
    fog = fg*0.4 
    
    return fog 

"""
    viii. Average Number of Words Per Sentence
"""

def average_number_of_words_per_sentence(article_text):
    avg_num = len(word_tokenize(article_text))/len(sent_tokenize(article_text))
    
    return avg_num

"""
    ix. Complex Word Count
"""

def complex_word_count(text):
    words = word_tokenize(text)
    complex_words = [word for word in words if syllable_count(word) > 2]
    return len(complex_words)

"""
    x.Word Count
"""

def word_count(article_text):
    cleaned_text = remove_stopwords(article_text, given_stop_words)
    
    # remove punctuations
    words_without_punctuations = [word for word in cleaned_text if word not in string.punctuation]
    
    return len(words_without_punctuations)

"""
    xi. Syllable Count Per Word
"""
def syllable_count_per_word(article_text):
    syllables = 0
    article_words=word_tokenize(article_text)
    
    for word in article_words:
        
        vowels = "aeiou"
        word = word.lower()
        
        if word[0] in vowels:
            syllables += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                syllables += 1
        if word.endswith("es") or word.endswith("ed"):
            syllables -= 1
        if syllables == 0:
            syllables += 1
    
    return syllables

"""
    xii. Personal Pronouns 
"""

def personal_pronouns(article_text):
    pronouns = ['I', 'we', 'my', 'ours', 'us']
    article_text = article_text.lower()
    pronoun_count = 0
    for pronoun in pronouns:
        pattern = r'\b' + pronoun + r'\b'
        pronoun_count += len(re.findall(pattern, article_text))
    
    # Exclude the country name "US"
    pronoun_count -= len(re.findall(r'\b us    \b', article_text))
    return pronoun_count

"""
    xiii. Average Word Length    
"""

def average_word_length(article_text):
    count=0
    article_words=word_tokenize(article_text)
    
    for word in article_words:
        count+=len(word)
    
    avg_length = count/len(article_words)

    return avg_length             

"""
>>>>>>>>>>>>>>> *Calculate all 13 variables for each article* <<<<<
"""

def process_all_tasks(article_content, given_stop_words, positive_words, negative_words):
    
    filtered_words=remove_stopwords(article_content, given_stop_words)

    positive_score = check_positive_score(filtered_words, positive_words)
    negative_score = check_negative_score(filtered_words, negative_words)
    polarity_score = check_polarity_score(positive_score, negative_score)
    subjective_score = check_subjective_score(filtered_words, positive_score, negative_score)
    avg_sent_len = compute_avg_sentence_length(article_content)
    percent_of_complex_words = percentage_of_complex_words(article_content)
    fogindex = fog_index(article_text=article_content)
    average_numberofwords_per_sentence = average_number_of_words_per_sentence(article_content)
    complexword_count = complex_word_count(article_content)
    wordCount = word_count(article_content)
    syllablecount_per_word = syllable_count_per_word(article_content)
    personalpronouns = personal_pronouns(article_content)
    averageword_length = average_word_length(article_content)        

    result={
        "POSITIVE_SCORE": positive_score,
        "NEGATIVE_SCORE": negative_score,
        "POLARITY_SCORE": polarity_score,
        "SUBJECTIVITY_SCORE": subjective_score,
        "AVG_SENTENCE_LENGTH": avg_sent_len,
        "PERCENTAGE_OF_COMPLEX_WORDS": percent_of_complex_words,
        "FOG_INDEX": fogindex,
        "AVG_NUMBER_OF_WORDS_PER_SENTENCE": average_numberofwords_per_sentence,
        "COMPLEX_WORD_COUNT": complexword_count,
        "WORD_COUNT": wordCount,
        "SYLLABLE_PER_WORD": syllablecount_per_word,
        "PERSONAL_PRONOUNS": personalpronouns,
        "AVG_WORD_LENGTH": averageword_length
    }
    
    return result


"""
>>>>>>>>>>>>>>>>>>>>>>>>>
----------- Main Execution starts ---------------
<<<<<<<<<<<<<<<<<<<<<<<<<
"""

# Read 'URL' and 'URL_ID' from ``Input.xlsx`` 

input_df = pd.read_excel('Input.xlsx')
results = []

# Create a folder `crawled_articles` if not exists
if not os.path.exists("crawled_articles"):
    os.mkdir("crawled_articles")

# Go through each URL and crawl 
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    inputs = {'URL_ID': url_id, 'URL': url}
    
    # Save content as text file
    if not os.path.exists(f'crawled_articles/{url_id}.txt'):
        
        # Start crawling
        article_text = crawl_article(url)
    
        with open(f'crawled_articles/{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(article_text)   

    
    # Read the content from text file and store in ``article_content``
    
    texts = open(f"crawled_articles/{url_id}.txt", "r", encoding="utf-8")
    article_content=''
    
    for line in texts:
            article_content=article_content.join(texts.readline())
    
                
    # Calculate all the variables: call ``process_all_tasks()`` 
    result = process_all_tasks(article_content, given_stop_words,positive_words, negative_words)
    
    # will create a new dictionary
    final_result = {**inputs, **result}
    
    results.append(final_result)
    
    
# Convert results to DataFrame and save as CSV
output_df = pd.DataFrame(results)
output_df.to_csv('Output.csv', index=False)