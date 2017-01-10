import json
from collections import defaultdict
import numpy
import gensim
import os.path


def search_repo(repo):
    dic_end = defaultdict(int)
    sum = 0;
    endings = []
    for path in repo:
        if(path['type'] == "Blob"):
            parts = path['path'].split(".")
            for part in parts:
                last = part
            dic_end[last] += 1
            sum+=1;
    for e in list(dic_end):
        if(dic_end[e] <= sum/100):
            del(dic_end[e])
        else:
            for i in range (0, dic_end[e]):
                endings.append(e)
    return endings

def search_desc(desc, readme):
    dic_desc = defaultdict(int)
    sum = 0
    words = open("data/stopwords.txt").read().split("\n");
    if(desc != ("") and desc is not None):
        for word in desc.split(" "):
            if not word in words:
                dic_desc[word] += 1
                sum += 1
    if(readme != ("") and readme is not None):
        for word in readme.split(" "):
            if not word in words:
                dic_desc[word] += 1
                sum += 1
    words = []
    for e in list(dic_desc):
        if(dic_desc[e] < sum/100):
            del(dic_desc[e])
        else:
            for i in range (0, dic_desc[e]):
                words.append(e)
    #print(dic_desc)
    return words
# corpus ergebnis zuordnen
# similarities mit ergebnissen
"""
@param file json file to analyze or train with
@param training 0-analyze, 1-training, 2-vector optimization
@return vector for networks
"""
def prep(file, training = 0):
    if(os.path.isfile(file)):
        data = json.loads(open(file).read())
    else:
        if(training != 2):
            print("file not found: "+file)

    # load dictionary and corpus
    if(os.path.isfile("dic.txt")):
        dictionary = gensim.corpora.Dictionary.load("dic.txt")
    else:
        dictionary = gensim.corpora.Dictionary()
    if(os.path.isfile("dicEnd.txt")):
        dictionaryEndings = gensim.corpora.Dictionary.load("dicEnd.txt")
    else:
        dictionaryEndings = gensim.corpora.Dictionary()
    if(os.path.isfile("cor.mm")):
        corpus = list(gensim.corpora.MmCorpus("cor.mm"))
    else:
        corpus = []
    if(os.path.isfile("corEnd.mm")):
        corpusEndings = list(gensim.corpora.MmCorpus("corEnd.mm"))
    else:
        corpusEndings = []


    json_out_raw_arr = []
    for rep in data:
        #TODO file endings
        end = search_repo(rep['repository'])
        endTmp = []
        endTmp.append(end)

        res = search_desc(rep['description'], rep['readme'])
        endings = search_repo(rep['repository'])
        endingstmp = []
        endingstmp.append(endings)
        tmp = []
        tmp.append(res)
        dump = ""

        if(training == 2):
            dictionary.filter_extremes(10, 0.8, None)
            dictionary.compactify()
            print(dictionary)
            dictionaryEndings.filter_extremes(10, 0.8, None)
            dictionaryEndings.compactify()
            print(dictionaryEndings)
        elif(training == 1):
            dictionary.merge_with(gensim.corpora.Dictionary(tmp))
            corpus.append(dictionary.doc2bow(res))
            print(dictionaryEndings)
            dictionaryEndings.merge_with(gensim.corpora.Dictionary(endingstmp))
            corpusEndings.append(dictionary.doc2bow(endings))
        elif(training == 0):
            tfidf = gensim.models.TfidfModel(corpus)
            json_out_raw = [0 for x in range(dictionary.__len__() + dictionaryEndings.__len__())]
            for elem in tfidf[dictionary.doc2bow(res)]:
                #print(json_out_raw)
                if(elem[0] is not None and elem[1] is not None):
                    if(elem[0]>=len(json_out_raw)):
                        json_out_raw.append(elem[1])
                    else:
                        json_out_raw[elem[0]] = elem[1]
            for elem in tfidf[dictionaryEndings.doc2bow(endings)]:
                #print(json_out_raw)
                if(elem[0] is not None and elem[1] is not None):
                    if(elem[0]>=len(json_out_raw)):
                        json_out_raw.append(elem[1])
                    else:
                        json_out_raw[elem[0]+dictionary.__len__()] = elem[1]

            #for elem in tfidf[dictionary.doc2bow(end)]:
                #print(json_out_raw)
            #    if(elem[0] is not None and elem[1] is not None):
            #        if(elem[0]>=len(json_out_raw)):
            #            json_out_raw.append(elem[1])
            #        else:
            #            json_out_raw[elem[0]+dictionary.__len__()] = elem[1]
            json_out_raw_arr.append(json_out_raw)
        else:
            print("param error")
        #lsi = gensim.models.LsiModel(corpus)
        #vec_lsi = lsi[dictionary.doc2bow(res)]
        #print(vec_lsi)
        #über corpora iterieren
        #tfidf * res des corpus(Network)
        # auf einen 7Tupel addieren
        #Gewichtung des Network hinfällig
        #json_out_raw_arr.append(json_out_raw)
        #Funktionsaufruf
        #resu = Network.?
        #kriegt 7Tupel
        #results.append([0.5, 0.3, 0, 0, 0.1, 0.7, 0.5])
        #print(json_out_raw)
    dictionary.save("dic.txt")
    gensim.corpora.MmCorpus.serialize("cor.mm", corpus)
    dictionaryEndings.save("dicEnd.txt")
    gensim.corpora.MmCorpus.serialize("corEnd.mm", corpusEndings)
    #print(dump)
    return json_out_raw_arr
