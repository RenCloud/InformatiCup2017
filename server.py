import data.dataprepNumeric as dataprep
import os
import learning.frontend.Main
import json

inp = input("Select mode:\n t - training\n d - filter_extremes\n v - training with validation set \n other key - normal mode\n$")
if(inp == "t"):
    for jsonFile in os.listdir("./data/json"):
        print ("data/json/"+jsonFile)
        vec = dataprep.prep("data/json/"+jsonFile, 1)
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
    cat = learning.frontend.Main.fit_dbn(vec, main_dir="third_try", supervised_train_set=svt, validation_set=vs,
                                         do_pretraining=True)
else:
    tmp = []
    for jsonFile in os.listdir("./data/json"):
        tmp = tmp + dataprep.prep("data/json/"+jsonFile)
    vec = json.dumps(tmp)
    cat = learning.frontend.Main.fit_dbn(vec, main_dir="test")
