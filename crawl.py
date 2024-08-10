import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

# Load the input file
# df = pd.read_excel('Input.xlsx')

# for index, row in df.iterrows():
#     url_id = row['URL_ID']
#     url = row['URL']
    
#     # Request the page
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Extract title and article text
#     title = soup.find('h1').get_text()
#     paragraphs = soup.find_all('p')
#     article_text = " ".join([p.get_text() for p in paragraphs])

#     # Save to a text file
#     with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
#         file.write(title + "\n" + article_text)

# Request the page

url_id='second'
url='https://insights.blackcoffer.com/streamlined-integration-interactive-brokers-api-with-python-for-desktop-trading-application/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract title and article text
title = soup.find('h1').get_text()
paragraphs = soup.find_all('p')
article_text = " ".join([p.get_text() for p in paragraphs])

## All the articles have same content after wors "Summarized"

position = article_text.find("Summarized")

if position != -1:
    article_text=article_text[:position + len("Summarized")]

# Save to a text file
with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
    file.write(title + "\n" + article_text)