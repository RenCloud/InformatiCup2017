import data.dataprep
import os
import learning.frontend.Main
inp = input("Select mode:\n t - training\n d - filter_extremes\n other key - normal mode\n$")
if(inp == "t"):
    for jsonFile in os.listdir("./data/json"):
        print ("data/json/"+jsonFile)
        vec = data.dataprep.prep("data/json/"+jsonFile, 1)
elif(inp == "d"):
    data.dataprep.prep("data/test.json", 2)
else:
    vec = data.dataprep.prep("data/json/1-367.json")
    print(vec)
cat = learning.frontend.Main.fit_dbm(vec, main_dir="test")
