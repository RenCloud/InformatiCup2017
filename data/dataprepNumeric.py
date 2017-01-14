import json
from collections import defaultdict
import numpy
import gensim
import os.path
import math

def logis(value):
    return((1/(1+math.exp(-100*(value/200))))-0.5)*2

"""
@param file json file to analyze or train with
@param training 0-analyze, 1-training, 2-vector optimization
@return vector for networks
"""
def prep(file, training = 0):
    json_out_raw_arr = []

    if(os.path.isfile(file)):
        data = json.loads(open(file).read())
    else:
        if(training != 2):
            print("file not found: "+file)

    for repo in data:
        files = 1
        vec = []
        for path in repo['repository']:
            if(path['type'] == "Blob"):
                files+=1
        vec.append(logis(files))
        vec.append(logis(len(repo['commits'])/files)) #relativ zu Anzahl Ordner+Files
        vec.append(logis(len(repo['comments'])/len(repo['commits']))) #relativ zu commits
        openI = 0
        closedI = 1
        for i in range(len(repo['issue'])):
            if(repo['issue'][i]['state'] == 'open'):
                openI += 1
            elif(repo['issue'][i]['state'] == 'closed'):
                closedI += 1
        vec.append(logis(openI/closedI)) #nur open-closed
        author = []
        for commit in repo['commits']:
            if(commit['author_login'] not in author):
                author.append(commit['author_login'])
        vec.append(logis(len(author)))
        committer = []
        for commit in repo['commits']:
            if((commit['committer_login'] not in committer)):
                committer.append(commit['committer_login'])
        vec.append(logis(len(committer)))

        #ordnernamen

        """dic_end = defaultdict(int)
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
        return endings"""
        json_out_raw_arr.append(vec)

    return json_out_raw_arr
