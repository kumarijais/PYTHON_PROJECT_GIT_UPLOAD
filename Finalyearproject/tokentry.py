import nltk
import mysql.connector
import operator

cnx=mysql.connector.connect(user='root',password='Mehwash',host='127.0.0.1',database='finalyear')
curs=cnx.cursor()

from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from collections import Counter



def process_content(filePath,sub):
    train_text = state_union.raw(filePath)
    sample_text = state_union.raw(filePath)
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)

    try:
        bigList = []
        c=1
        with open("mytext.txt",'w') as ft1:
            for i in tokenized:
                words = nltk.word_tokenize(i)
                tagged=nltk.pos_tag(words)
                print(tagged)
                for j in tagged:
                    bigList.append(j)
                ques="Q"+str(c)+")"
                ft1.write(ques)
                verbList=[]
                for x in tagged:
                    if((x[1]=='VBZ')or(x[1]=='VB')or (x[1]=='VBP')or (x[1]=='VBG')or(x[1]=='VBN'))or (x[1]=='VBD'):
                     verbList.append(x[0])
                print(verbList)
                #ft1.write("Verbs are:")
                s=str(verbList).strip('[]')
                #ft1.write(s)
                finalListV=[]
                for w in verbList:
                    constrain = w
                    curs.execute("select * from action_verbs where verbs=%s",(constrain,))
                    data = curs.fetchall()
                    #print("data")
                    #print(data)
                    for j in data:
                        finalListV.append(str(j[0]))
                        level=j[1]
                print("finalListV1")
                print(finalListV)
                finalListV = list(map(int, finalListV))
                print(finalListV)
                nounList = []
                for x in tagged:
                    if ((x[1] == 'NNP') or (x[1] == 'NN') or (x[1] == 'NNS')):
                        nounList.append(x[0])
                #print("Nouns are:")
                print(nounList)
                s1=str(nounList).strip('[]')
                finalListN = []
                for n in nounList:
                    keyword = n
                    # write if dept is cse taking from user  input
                    curs.execute("select * from jkeywordsc ,levels  where jkeywordsc.co=levels.cno and jkey=%s and dept=%s", (keyword,sub,))
                    data = curs.fetchall()
                    for j in data:
                        finalListN.append(str(j[4]))
                #print("finalListN")
                print(finalListN)

                stats = dict(Counter(finalListN))
                #maxval = max(dict.iteritems(), key=operator.itemgetter(1))[1]
                #print(keys = [k for k, v in Counter.items() if v == maxval])

                match=max(stats.items(), key=operator.itemgetter(1))[0]
                #for k, v in newList.items():
                    #print(k, v)
                match=int(match)
                if match in finalListV:
                    ft1.write("Accepted at level:"+str(match)+"("+level+")"+"of Blooom's Taxonomy")
                else:
                    ft1.write("Rejected,Levels not satisfied")
                ft1.write("\n")



                c=c+1
                #print(finalListN)
        return ("mytext.txt")

    except Exception as e:
        print(str(e))
