from flask import *
import pickle
import os
import re

app = Flask(__name__)

@app.route("/")

def index():
    title = "Title"
    message = "Hello, fiord"
    files = list(filter(lambda x: os.path.isfile(os.path.join("data/pcap", x)) and re.search(r"\.dat$", x), os.listdir("./data/pcap")))
    return render_template("index.html", message=message, title=title, files=files)

@app.route("/api/data/<filepath>")
def apiShowData(filepath):
    f = open("data/pcap/{0}".format(filepath), "rb")
    res = pickle.load(f)
    return jsonify(res)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
