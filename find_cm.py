import sys
import re
import time
from multiprocessing import Pool
from urlparse import urljoin

from bs4 import BeautifulSoup
import requests

BASE_URL = "http://oss.reflected.net/jenkins/"
MAX_PROCESSES = 20

# Use default value if no command-line argument provided
try:
    MODEL, OUTPUT = sys.argv[1], sys.argv[2]
except:
    MODEL = "9100" 
    OUTPUT = "cm_" + MODEL + "_links.txt"

def build_bs(url):
    """construct a BeautifulSoup instance with the given link and return"""
    r = requests.get(url)
    return BeautifulSoup(r.text)

#def _filter(string, search_strs, match_all=False):
    #"""return true if any/all of the search_strs found in string when match_all is False/True"""

def keyword_filter(url, keywords=None):
    """return true if url contains all keywords,
       return false otherwise 
    """
    if not keywords: return True
    return all(keyword in url for keyword in keywords)

def file_filter(url, filetypes=None):
    """return true if url is of any type in the file types,
       return false otherwise 
    """
    if not filetypes: return True
    return any(filetype in url.split(".")[-1] for filetype in filetypes)

def save_links(links):
    """ write a list of links to file"""
    with open(OUTPUT, 'a+') as f:
        for link in links:
            f.write(link + "\n")

def get_anchor_url(page_url, keywords=None):  
    """return all anchors' absolute url, 
       if formats provided, return the matches ones
    """
    bs = None

    while True:
        try:
            bs = build_bs(page_url)
        except:
            # sleep for 5 seconds and try again
            time.sleep(5)

        if bs: break

    # retrive value of 'href' attribute in all anchors
    anchors_url = [a['href'] for a in list(bs.findAll("a"))]

    # join absolute url: page_url + anchors_url, assume that all 
    # anchor_url is relative url. Apply keyword filter to the results
    anchors_abs_url = [urljoin(page_url, url) for url in anchors_url if keyword_filter(url, keywords)]

    return anchors_abs_url

def get_zip_url(dir_url):
    """return all the absolute url of zip file"""
    zip_urls = get_anchor_url(dir_url, keywords=[MODEL,])
    zip_urls = [url for url in zip_urls if file_filter(url, filetypes=['zip'])]
    save_links(zip_urls)

#def extract(url, pattern=None):
    #"""use pattern to retrive information from the url"""
    #PATTERNS = {
        #"DATE":"DATE_PATTERN",
        #"VERSION":"VERSION_PATTERN",
        #"RELEASE":"RELEASE_PATTERN",
    #}
    #return re.findall(PATTERNS.get(pattern), url)

if __name__ == "__main__":
    # find all the dir urls
    urls = get_anchor_url(BASE_URL)

    pool = Pool(MAX_PROCESSES)
    pool.map(get_zip_url, urls) 

    pool.close()
    pool.join()
