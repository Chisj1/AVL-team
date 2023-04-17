import requests
from spam_lists import SPAMHAUS_DBL
import model.preprocessor as Preprocessor

BLACKLIST_FILE = "data/blacklist.csv"
WHITELIST_FILE = "data/whitelist.csv"
PAGE_RANK_API = "https://openpagerank.com/api/v1.0/getPageRank"
PAGE_RANK_API_KEY = "s804cos8k00g04swg448s8wkssgswcsw4cwcw8gs"


def isConnected(url):
    try:
        r = requests.get(url, timeout=7)
        return 1
    except:
        return 0


def isBlacklist(url):
    with open(BLACKLIST_FILE, "r", encoding="UTF-8") as f:
        return url in f.read().split("\n")


def isWhitelist(url):
    with open(WHITELIST_FILE, "r", encoding="UTF-8") as f:
        return url in f.read().split("\n")


def isSpam(url):
    netloc = Preprocessor.parse_url(url)['netloc']
    return netloc in SPAMHAUS_DBL


def checkPageRank(url):
    try:
        URL = PAGE_RANK_API
        PARAMS = {'domains[]': Preprocessor(url)['netloc']}
        r = requests.get(URL, params=PARAMS, headers={
            'API-OPR': PAGE_RANK_API_KEY}, timeout=7)
        json_data = r.json()
        domainarray = json_data['response']
        target = domainarray[0]
        rank = target['rank']
        if rank == "None" or float(rank or 0.1) < 0.2:
            return 0
        else:
            return 1

    except Exception as e:
        print("getPageRank error:", e)
        return 0
