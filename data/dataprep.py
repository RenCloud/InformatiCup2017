import json
from collections import defaultdict
import numpy
import gensim


def search_repo(repo):
    dic_end = defaultdict(int)
    sum = 0;
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
    #print(dic_end)

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


def prep():
    json_data = open("data/json/1-367.json").read()
    data = json.loads(json_data)
    corpus = [[(0, 1.0), (1, 1.0), (2, 1.0)],
            [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
            [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
            [(0, 1.0), (4, 2.0), (7, 1.0)],
            [(3, 1.0), (5, 1.0), (6, 1.0)],
            [(9, 1.0)],
            [(9, 1.0), (10, 1.0)],
            [(9, 1.0), (10, 1.0), (11, 1.0)],
            [(8, 1.0), (10, 1.0), (11, 1.0)]]
    tfidf = gensim.models.TfidfModel(corpus)
    vec = [(0, 1),(4,1)]
    index = gensim.similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=12)
    sims = index[tfidf[vec]]
    #print(list(enumerate(sims)))
    dictionary = gensim.corpora.Dictionary()
    corpus = []
    json_out_raw_arr = []
    for rep in data:

        #vec += search_lang(rep['language'])
        search_repo(rep['repository'])
        res = search_desc(rep['description'], rep['readme'])
        tmp = []
        tmp.append(res)
        dictionary.merge_with(gensim.corpora.Dictionary(tmp))
        corpus.append(dictionary.doc2bow(res))
        #vec +=
        tfidf = gensim.models.TfidfModel(corpus)
        #print(tfidf[dictionary.doc2bow(res)])
        json_out_raw = []
        for elem in tfidf[dictionary.doc2bow(res)]:
            if(elem[0] is not None and elem[1] is not None):
                if(elem[0]>=len(json_out_raw)):
                    json_out_raw.append(elem[1])
                else:
                    json_out_raw[elem[0]] = elem[1]
        json_out_raw_arr.append(json_out_raw)
        dump = json.dumps(json_out_raw_arr)
    return dump
#f = open("vec.json", "w")
#f.write(dump)
#print(dump)
