from flask import Flask, render_template, request
from model.model import Converter
import utils.checker as Checker
import model.function as Model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


@app.route("/api/check", methods=["GET"])
def check():
    url = request.args["url"].replace(" ", "")

    if Checker.isWhitelist(url):
        print("Url is in whitelist")
        return "0"

    if Checker.isBlacklist(url):
        print("Url is in blacklist")
        return "1"

    # if Checker.isSpam(url):
    #     print("Url is spam")
    #     return "1"

    if Checker.checkPageRank(url):
        print("Url is low pagerank")
        return "1"

    if Model.check(url):
        print("Model: Url is phishing")
        return "1"
    else:
        print("Model: Url is normal")
        return "0"


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=8080)
