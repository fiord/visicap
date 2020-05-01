import pickle
import sys
import re
import Levenshtein
from sklearn.cluster import KMeans
import numpy as np
from datetime import datetime

def check(dat, num):
    res = {}
    lim = 500
    length = len(dat)
    i = 0
    print("len=",length)
    for key, val in dat.items():
        i+=1
        if i % 100 == 0:
            print(i, "/", len(dat))
        numg = min(num, len(val))
        limg = min(lim, len(val))
        # print(key, "len=", len(val))
        arr = [v[0].hex() for v in val][:limg]
        dist = np.array([np.array([1.0 - Levenshtein.jaro_winkler(v1, v2) for v2 in arr]) for v1 in arr])
        # print("dist complete")
        pred = KMeans(n_clusters=numg).fit_predict(dist)
        res[str(key)] = {
            "ele": [{
                "time": val[i][0],
                "data": str(val[i][1]),
                "label": int(pred[i])
            } for i in range(limg)],
            "dist": [[v for v in v2] for v2 in dist]
        }
    return res

if __name__ == "__main__":
    num = 5
    if len(sys.argv) == 2:
        num = int(sys.argv[1])

    filename = "./pcap/n056_20191111_000002.bin"
    output = filename.split("/")
    output[-1] = output[-1].split(".")
    output[-1][0] = "KMean{0:0>2}_{1}".format(num, datetime.now().strftime("%Y%m%d-%H%M%S")) + output[-1][0]
    output[-1][-1] = "dat"
    output[-1] = ".".join(output[-1])
    output = "/".join(output)
    f = open(filename, "rb")
    dat = pickle.load(f)
    f.close()
    tuples = check(dat, num)
    with open(output, "wb") as f:
        pickle.dump(tuples, f)
