import data.dataprepNumeric as dataprep
import os
import learning.frontend.Main
import json

def training(data, newDataset = False, valid = True, svtD=None, svtR = None, vsD = None, vsR = None):
    if(newDataset):
        print("new DataSet")

    if(len(data)<100):
        print("Error: DataSet zu klein")
        return

    tmp = []
    for i in range(len(data)):
        print(data[i])
        tmp += dataprep.prep(data[i])
        print(tmp)
    vec = json.dumps(tmp)

    if(valid):
        svt = []
        tmp = []
        for i in range(len(svt)):
            tmp += dataprep.prep(svtD[i])
        svt.append(json.dumps(tmp))
        tmp = []
        for i in range(len(svt)):
            tmp += dataprep.prep(svtR[i])
        svt.append(json.dumps(tmp))

        vs = []
        vs.append(json.dumps(dataprep.prep(vsD)))
        vs.append(open(vsR).read())
        learning.frontend.Main.fit_dbn(vec, main_dir="third_try", supervised_train_set=svt, validation_set=vs, do_pretraining=True)
    else:
        learning.frontend.Main.fit_dbn(vec, main_dir="test")
"""inp = input("Select mode:\n t - training\n d - filter_extremes\n v - training with validation set \n other key - normal mode\n$")
if(inp == "t"):
    for jsonFile in os.listdir("./data/json"):
        print ("data/json/"+jsonFile)
        vec = dataprep.prep("data/json/"+jsonFile, 1)
        print(vec)
elif(inp == "d"):
    dataprep.prep("data/test.json", 2)
elif(inp == "v"):
    svt = []
    tmp = []
    for i in range(1,5):
    #for jsonFile in os.listdir("./tagged/data"):
        print(i)
        tmp = tmp + dataprep.prep("./tagged/data/jsontest"+str(i)+".json")
    svt.append(json.dumps(tmp))
    tmp = []
    for i in range(1,5):
    #for jsonFile in os.listdir("./tagged/tag"):
        print(i)
        tmp = tmp + json.loads(open("./tagged/tag/tagarray"+str(i)+".json").read())
    svt.append(json.dumps(tmp))
    tmp = []
    if(os.path.isfile("vecfile.txt")):
        vec = open("vecfile.txt").read()
    else:
        for jsonFile in os.listdir("./data/json"):
            print(jsonFile)
            tmp = tmp + dataprep.prep("data/json/"+jsonFile)
        vec = json.dumps(tmp)
        vecFile = open("vecfile.txt", "w")
        vecFile.write(vec)
        vecFile.close()
    vs = []
    vs.append(json.dumps(dataprep.prep("./gegeben.json")))
    vs.append(open("./gegebenarray.json").read())

    # vs
    cat = learning.frontend.Main.fit_dbn(vec, main_dir="small_network", supervised_train_set=svt, validation_set=svt,
                                         do_pretraining=False)
else:
    tmp = []
    for jsonFile in os.listdir("./data/json"):
        tmp = tmp + dataprep.prep("data/json/"+jsonFile)
    vec = json.dumps(tmp)
    cat = learning.frontend.Main.fit_dbn(vec, main_dir="test")"""
