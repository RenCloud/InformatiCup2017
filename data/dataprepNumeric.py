import json
import numpy
import os.path
import math
from collections import defaultdict
import gensim


def logis(value):
    return((1 / (1 + math.exp(-25 * (value / 200)))) - 0.5) * 2


def logisFile(value):
    return((1 / (1 + math.exp(-1 * (value / 1000)))) - 0.5) * 2

def search_repo(repo):
    dic_end = defaultdict(int)
    sum = 0;
    endings = []
    for path in repo:
        if(path['type'] == "Tree"):
            parts = path['path'].split("/")
            for part in parts:
                last = part
            dic_end[last] += 1
            sum+=1;
    for e in list(dic_end):
        if(dic_end[e] <= sum/100):
            del(dic_end[e])
        else:
            endings.append(e)
    return endings

"""
@param file json file to analyze or train with
@param training 0-analyze, 1-training, 2-vector optimization
@return vector for networks
"""


def prep(file, training=0):
    if(os.path.isfile("dicEnd.txt")):
        dictionaryEndings = gensim.corpora.Dictionary.load("dicEnd.txt")
    else:
        dictionaryEndings = gensim.corpora.Dictionary()

    json_out_raw_arr = []

    if training == 0 or training == 1:
        if(os.path.isfile(file)):
            data = json.loads(open(file).read())
        else:
            if training != 2:
                print("file not found: " + file)
    elif training == 2:
        data = json.loads(file)

    if training == 3:
        print("Before:"+str(dictionaryEndings))
        dictionaryEndings.filter_extremes(500, 1.0, None)
        dictionaryEndings.compactify()
        print("After:"+str(dictionaryEndings))
        dictionaryEndings.save("dicEnd.txt")
        return

    for repo in data:

        endingstmp = [search_repo(repo['repository'])]

        if training == 1:
            dictionaryEndings.merge_with(gensim.corpora.Dictionary(endingstmp))
        if training == 0 or training == 2:

            files = 1
            vec = []
            search_repo(repo['repository'])
            for path in repo['repository']:
                if(path['type'] == "Blob"):
                    files+=1
            vec.append(len(repo['commits']))
            vec.append(len(repo['comments']))
            openI = 0
            closedI = 1
            for i in range(len(repo['issue'])):
                if(repo['issue'][i]['state'] == 'open'):
                    openI += 1
                elif(repo['issue'][i]['state'] == 'closed'):
                    closedI += 1
            vec.append(openI)
            vec.append(closedI)
            author = []
            for commit in repo['commits']:
                if(commit['author_login'] not in author):
                    author.append(commit['author_login'])
            vec.append(len(author))
            committer = []
            for commit in repo['commits']:
                if((commit['committer_login'] not in committer)):
                    committer.append(commit['committer_login'])
            vec.append(len(committer))

            json_out_raw_arr.append(vec)

    dictionaryEndings.save("dicEnd.txt")
    return json_out_raw_arr
