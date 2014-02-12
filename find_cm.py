import sys
from urlparse import urljoin

from bs4 import BeautifulSoup
import requests

BASE_URL = "http://oss.reflected.net/jenkins/"

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
    """return true if url contains any keywords,
       return false otherwise 
    """
    if not keywords:
        return True

    return any(keyword in url for keyword in keywords)

def get_all_anchor_url(page_url, keywords=None):  
    """return all anchors' absolute url, 
       if formats provided, return the matches ones
    """
    bs = build_bs(page_url)

    # retrive value of 'href' attribute in all anchors
    anchors_url = [a['href'] for a in list(bs.findAll("a"))]

    # join absolute url: page_url + anchors_url, assume that all 
    # anchor_url is relative url. Apply keyword filter to the results
    anchors_abs_url = [urljoin(page_url, url) for url in anchors_url if url_filter(url, keywords)]
    return anchors_abs_url

def write_links(links):
    """ write a list of links to file"""
    with open(OUTPUT, 'w') as f:
        for link in result_links:
            f.write(link + "\n")

if __name__ == "__main__":
    result_links = []

    # find all the dir urls
    dir_urls = get_all_anchor_url(BASE_URL)

    # loop through dir urls and find all the match zip file
    total = len(dir_urls)
    for index, dir_url in enumerate(dir_urls):
        zip_urls = get_all_anchor_url(dir_url, keywords=[MODEL,])
        # if find anything, add to results, and print it out
        if zip_urls:
            result_links.extend(zip_urls)
            print zip_urls

        # print out number of links left
        print "%d to go..." % (total-index)

    write_links(result_links)    
