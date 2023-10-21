import json
import os
import requests
import re
import sys
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from PIL import Image


def get_pic(url_list):
    """
    download pictures from url_list.
    :param url_list: list of url for pictures
    :return: list of picture filenames
    """
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
                pic_name = f"pic/{part_num}/{num}.jpg"
                filenames.append(pic_name)
                with open(pic_name, "wb") as f:
                    f.write(res.content)
            else:
                break
            num += 1
    return filenames


def pic2pdf(filenames, book_name):
    """
    convert pictures to pdf.
    :param filenames: list of picture filenames
    :param book_name: name of the book
    :return: None
    """
    im_list = []
    for filename in tqdm(filenames, desc="Converting to PDF"):
        im_list.append(Image.open(filename).convert("RGB"))
    im_list[0].save(f"{book_name}.pdf", save_all=True, append_images=im_list[1:])


def get_part_url(href):
    """
    get url of picture from href.
    :param href: url to part of the book
    :return: picture url from href
    """
    part_url = f"http://reserves.lib.tsinghua.edu.cn{href}"
    part_url = re.sub(r"index.html", "files/mobile/", part_url)
    return part_url


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
    if category.__len__() == 1:
        url_list.append(get_part_url(category[0]["href"]))
    else:
        print("是否下载全部章节? (y/n)", end=" ")
        choice = input()
        if choice == "y":
            for part in category:
                url_list.append(get_part_url(part["href"]))
        elif choice == "n":
            for part in category:
                chapter = part.text.strip()
                print(f"是否下载 {chapter} ? (y/n)", end=" ")
                choice = input()
                if choice == "y":
                    url_list.append(get_part_url(part["href"]))
                elif choice != "n":
                    print("非法输入!!!")
                    sys.exit(1)
        else:
            print("非法输入!!!")
            sys.exit(1)
    pic2pdf(get_pic(url_list), bookName)
    os.system("rm -rf pic")
