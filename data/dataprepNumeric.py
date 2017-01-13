import json
from collections import defaultdict
import numpy
import gensim
import os.path


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
        i = 0
        vec = []
        for path in repo['repository']:
            if(path['type'] == "Blob"):
                i=i+1
        vec.append(i/1000)
        vec.append(len(repo['commits'])/1000)
        vec.append(len(repo['comments'])/1000)
        vec.append(len(repo['issue'])/1000)
        author = []
        for commit in repo['commits']:
            if(commit['author_login'] not in author):
                author.append(commit['author_login'])
        vec.append(len(author)/1000)
        committer = []
        for commit in repo['commits']:
            if((commit['committer_login'] not in committer)):
                committer.append(commit['committer_login'])
        vec.append(len(committer)/1000)

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
