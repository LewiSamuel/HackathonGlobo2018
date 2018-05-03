import operator
from nltk import ngrams, FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.metrics import *

import pandas as pd
import unicodedata
import time

import tweepy



 
consumer_key= 'ZnD0V18VJcdlQkzTcEkOpeNgx'
consumer_secret= 'AwARJEnDh5IYV7hlgvmwimbmPEubMMbIXX2RyM2PfCrGLbNWXN'
 
access_token='63313336-pheI0pgM5xavuMfU5Hbl6dEAIwSPyBBRUEi0MMpUB'
access_token_secret='VYe99X6HQpDD1UGv4UOqyJclAnv9BIIClaMTfADmzu8lV'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)
 
kw = "HackathonGlobo"
 
public_tweets = api.search(q = kw, rpp = 5, lang = "pt", show_user = False)# since_id = "990392457937477632")
# 990486932433010688
df = []
for tweet in public_tweets:
    #if(tweet.text[0] != 'R'):
    df.append(tweet.text)
    print(tweet.text)
    print(tweet.user._json['name'])


from firebase import firebase
firebase = firebase.FirebaseApplication('https://hackathon-globo-2018.firebaseio.com/', None)



stopWords = set(stopwords.words('portuguese'))
stopWords.discard("fora")
stopWords.update(['hackathonglobo', '.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '\\', '#', '%', 'rt', '@', '...', 'https'])
count = 0

bigStr = []
comments = []
orgComments = []

for elem in df:
    if(type(elem) is str):
        temp = str(unicodedata.normalize('NFKD', elem).encode('ascii','ignore'))[2:-1]
        orgComments.append(temp)
        temp = temp.lower()
        # temp = word_tokenize(temp)
        new_temp = list(set(word_tokenize(temp)))
        wordsFiltered = []
        for w in new_temp:
            if w not in stopWords:
                wordsFiltered.append(w)
        bigStr += wordsFiltered
        comments.append(wordsFiltered)


wordsCount = FreqDist(ngrams(bigStr, 1))
d = dict(wordsCount)
wordsDict = dict((key[0], value) for (key, value) in d.items())

sortedDict = sorted(wordsDict.items(), key=operator.itemgetter(1), reverse = True)

# print(sortedDict[0:6])

for a in range(0,int(len(sortedDict)/3)):
    for b in range(a+1,int(len(sortedDict)/3)):
        if(edit_distance(sortedDict[a][0], sortedDict[b][0]) <= 1):
            sortedDict[a] = (sortedDict[a][0], (sortedDict[a][1] + sortedDict[b][1]))
            sortedDict[b] = (sortedDict[b][0], 0)

sortedDict = sorted(sortedDict, key=operator.itemgetter(1), reverse = True)
print(sortedDict[0:6])

medStr = []
medCount = []
sortedMedDict = []
medIndices = []
for i in range(0, 3):
    medStr.append([])
    medIndices.append([])
    for j in range(0, len(comments)):
        for k in comments[j]:
            if(edit_distance(sortedDict[i][0],k) <= 1):
                medStr[i] += comments[j]
                medIndices[i].append(j)
                break
    medCount.append(FreqDist(ngrams(medStr[i], 1)))
    d = dict(medCount[i])
    medDict = dict((key[0], value) for (key, value) in d.items())
    sortedMedDict.append(sorted(medDict.items(), key=operator.itemgetter(1), reverse = True))

    for a in range(0,int(len(sortedMedDict[i])/3)):
        for b in range(a+1,int(len(sortedMedDict[i])/3)):
            if(edit_distance(sortedMedDict[i][a][0], sortedMedDict[i][b][0]) <= 1):
                sortedMedDict[i][a] = (sortedMedDict[i][a][0], (sortedMedDict[i][a][1] + sortedMedDict[i][b][1]))
                sortedMedDict[i][b] = (sortedMedDict[i][b][0], 0)

    sortedMedDict[i] = sorted(sortedMedDict[i], key=operator.itemgetter(1), reverse = True)

    print(sortedMedDict[i][0:6])    
    print(orgComments[medIndices[i][0]])
answerFire = []
for a in range(0, 3):
    vector_temp = []
    for b in range(0, 3):
        vector_temp.append({"word":sortedMedDict[a][b+1][0], "freq":str(sortedMedDict[a][b+1][1])})
    answerFire.append({"word":str(sortedMedDict[a][0][0]),"freq":str(sortedMedDict[a][0][1]),"related":vector_temp, "comment":orgComments[medIndices[a][0]]})

result = {"name":""}
print(firebase.delete('/twitter', result["name"]))
result = firebase.post('/twitter', data={"data":answerFire})
print (result)
time.sleep(1)
 