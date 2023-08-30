import json
import os
import requests
import re
from bs4 import BeautifulSoup as bs

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    bookId = config["bookId"]
    headers = {"User-Agent": config["User-Agent"],
               "Cookie": config["Cookie"],
               "Accept": config["Accept"]}
    url = f"http://reserves.lib.tsinghua.edu.cn/Search/BookDetail?bookId={bookId}"
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "lxml")
