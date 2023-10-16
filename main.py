import json
import os
import requests
import re
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from PIL import Image


def get_pic(url_list):
    filenames = []
    if not os.path.exists("pic"):
        os.mkdir("pic")
    for url in url_list:
        part_num = url.split("/")[-4]
        if not os.path.exists(f"pic/{part_num}"):
            os.mkdir(f"pic/{part_num}")
        num = 1
        while True:
            pic_url = f"{url}{num}.jpg"
            res = requests.get(pic_url, headers=headers)
            pic_soup = bs(res.text, "lxml")
            if not pic_soup.find("a", id="eCode"):
                filenames.append(f"pic/{part_num}/{num}.jpg")
                with open(f"pic/{part_num}/{num}.jpg", "wb") as f:
                    f.write(res.content)
            else:
                break
            num += 1
    return filenames


def pic2pdf(filenames, book_name):
    im_list = []
    for filename in tqdm(filenames, desc="Converting to PDF"):
        im_list.append(Image.open(filename).convert("RGB"))
    im_list[0].save(f"{book_name}.pdf", save_all=True, append_images=im_list[1:])


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    bookId = config["bookID"]
    headers = {"User-Agent": config["User-Agent"],
               "Cookie": config["Cookie"]}
    url = f"http://reserves.lib.tsinghua.edu.cn/Search/BookDetail?bookId={bookId}"
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "lxml")
    table = soup.find("table")
    category = table.find_next_sibling().find_next_sibling().find_all("a")
    bookName = table.find_all("b")[1].text.strip()
    url_list = []
    for part in category:
        part_url = f"http://reserves.lib.tsinghua.edu.cn{part['href']}"
        part_url = re.sub(r"index.html", "files/mobile/", part_url)
        url_list.append(part_url)
    pic2pdf(get_pic(url_list), bookName)
    os.system("rm -rf pic")
