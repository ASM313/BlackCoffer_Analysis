import pandas as pd
from bs4 import BeautifulSoup
import requests


# Read the input file
input_data = pd.read_excel('Input.xlsx')

# Function to extract article text
def extract_text(url):
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

# Loop through each URL and extract text
for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    article_text = extract_text(url)
    with open(f'articles/{url_id}.txt', 'w', encoding='utf-8') as file:
        file.write(article_text)