import os

given_stop_words=[]

for item in os.listdir("StopWords"):
    f=open(f"StopWords/{item}", "r")
    for line in f:
        given_stop_words.append((line.split()[0]).lower())

print(f"Total Stop words are: {len(given_stop_words)}")         