import sys
import time
from multiprocessing import Pool
from urlparse import urljoin

from bs4 import BeautifulSoup
import requests

BASE_URL = "http://oss.reflected.net/jenkins/"
MAX_PROCESSES = 20

# if model & output file not provided use default value
try:
    MODEL, OUTPUT = sys.argv[1], sys.argv[2]
except:
    MODEL = "9100" 
    OUTPUT = "cm_" + MODEL + "_links.txt"

def build_bs(url):
    """construct a BeautifulSoup instance with the given link and return"""
    r = requests.get(url)
    return BeautifulSoup(r.text)

def url_filter(url, keywords=None):
    """return true if url contains all keywords,
       return false otherwise 
    """
    if not keywords:
        return True

    return all(keyword in url for keyword in keywords)

def write_links(links):
    """ write a list of links to file"""
    with open(OUTPUT, 'a+') as f:
        for link in links:
            f.write(link + "\n")

def get_all_anchor_url(page_url, keywords=None):  
    """return all anchors' absolute url, 
       if formats provided, return the matches ones
    """
    while True:
        try:
            bs = build_bs(page_url)
        except:
            bs = ""
            time.sleep(5)

        if bs: break

    # retrive value of 'href' attribute in all anchors
    anchors_url = [a['href'] for a in list(bs.findAll("a"))]

    # join absolute url: page_url + anchors_url, assume that all 
    # anchor_url is relative url. Apply keyword filter to the results
    anchors_abs_url = [urljoin(page_url, url) for url in anchors_url if url_filter(url, keywords)]
    return anchors_abs_url

def get_all_zip_url(dir_url):
    keywords = [MODEL, "zip"]
    zip_urls = get_all_anchor_url(dir_url, keywords)
    write_links(zip_urls)

if __name__ == "__main__":
    # find all the dir urls
    dir_urls = get_all_anchor_url(BASE_URL)

    pool = Pool(MAX_PROCESSES)
    pool.map(get_all_zip_url, dir_urls) 
    pool.close()
    pool.join()
