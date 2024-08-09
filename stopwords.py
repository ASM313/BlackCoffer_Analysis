given_stop_words=[]

f = open("stop.txt", "r")
for line in f:
    given_stop_words.append((line.split()[0]).lower())    

print(f"Total Stop words are: {len(given_stop_words)}")    