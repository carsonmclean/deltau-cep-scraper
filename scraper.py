from bs4 import BeautifulSoup
from progressbar import ProgressBar

import requests
import os
import urllib2


def getChapterURLs():
    url = 'http://www.deltau.org/ChapterExcellence'
    page = urllib2.urlopen('http://www.deltau.org/ChapterExcellence').read()
    soup = BeautifulSoup(page, 'html.parser')
    chapter_links = soup.select('ul li h3 a')
    chapter_URLs = []
    for a in chapter_links:
        chapter_URLs.append(str(a['href']))
    return chapter_URLs


def walkChapterCriteria(url):
    chapter_criteria_URL = 'http://www.deltau.org' + url + 'CriteriaList'
    r = requests.post(chapter_criteria_URL, data = {'filter': 'Fall Criteria'})

    soup = BeautifulSoup(r.text, 'html.parser')
    criteria_list = soup.find_all('li')
    chapter_name = urllib2.unquote(url.split('/')[2])

    for criteria in criteria_list:
        checkSubmission(criteria, chapter_name)


def checkSubmission(criteria, chapter_name):
    if criteria.find('a', 'fancybox'):
        folder_title = "CEP/" + criteria.h4.a.encode_contents().replace('/','|')
        checkFolder(folder_title)
        makeFolder(folder_title + '/' + chapter_name)


def checkFolder(folder_title):
    if not os.path.exists(folder_title):
        os.makedirs(folder_title)


def makeFolder(folder_title):
    if not os.path.exists(folder_title):
        os.makedirs(folder_title)
    else:
        print("This Chapter's folder already exists: " + folder_title)


def main():
    chapter_URLs = getChapterURLs()

    pbar = ProgressBar()
    # for url in pbar(chapter_URLs):
    #     walkChapterCriteria(url)
    walkChapterCriteria(chapter_URLs[0])


if __name__ == '__main__':
    main()
else:
    print("This program should be run directly!")
