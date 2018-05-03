import operator
from nltk import ngrams, FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.metrics import *

import pandas as pd
import unicodedata
import time

from firebase import firebase
firebase = firebase.FirebaseApplication('https://hackathon-globo-2018.firebaseio.com/', None)

new_df = pd.read_csv("comments_sort_auto.csv", sep='\t', encoding='utf-8')
c_df = new_df['message'].tolist()

time.sleep(30)

df_list = []
df_list.append(c_df[0:int(len(c_df)/4)])
df_list.append(c_df[0:int(len(c_df)/2)])
df_list.append(c_df[:])

stopWords = set(stopwords.words('portuguese'))
stopWords.discard("fora")
stopWords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '\\', '#', '%'])
count = 0
for df in  df_list:
    count += 1
    print(count)
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
    print(firebase.delete('/topico', result["name"]))
    result = firebase.post('/topico', data={"data":answerFire})
    print (result)
    


