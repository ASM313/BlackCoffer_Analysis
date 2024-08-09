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