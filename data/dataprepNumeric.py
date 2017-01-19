import json
import numpy
import os.path
import math


def logis(value):
    return((1 / (1 + math.exp(-25 * (value / 200)))) - 0.5) * 2


def logisFile(value):
    return((1 / (1 + math.exp(-1 * (value / 1000)))) - 0.5) * 2

"""
@param file json file to analyze or train with
@param training 0-analyze, 1-training, 2-vector optimization
@return vector for networks
"""


def prep(file, training=0):
    json_out_raw_arr = []

    if training == 0:
        if(os.path.isfile(file)):
            data = json.loads(open(file).read())
        else:
            if training != 2:
                print("file not found: " + file)
    elif training == 2:
        data = json.loads(file)

    for repo in data:
        files = 1
        vec = []
        for path in repo['repository']:
            if(path['type'] == "Blob"):
                files+=1
        # vec.append(logisFile(files))
        vec.append(len(repo['commits'])) #relativ zu Anzahl Ordner+Files
        vec.append(len(repo['comments'])) #relativ zu commits
        openI = 0
        closedI = 1
        for i in range(len(repo['issue'])):
            if(repo['issue'][i]['state'] == 'open'):
                openI += 1
            elif(repo['issue'][i]['state'] == 'closed'):
                closedI += 1
        vec.append(openI) #nur open-closed
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

    return json_out_raw_arr
