from bs4 import BeautifulSoup
from progressbar import ProgressBar

import requests
import os
import urllib
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
    # Only continue for Chapter's that have an accepted CEP criteria
    if criteria.find('a', 'fancybox'):
        folder_title = "CEP/" + criteria.h4.a.encode_contents().replace('/','|')
        checkFolder(folder_title)
        makeFolder(folder_title + '/' + chapter_name)

        submission_URL = 'http://www.deltau.org' + criteria.find('a', 'fancybox')['href']
        page = urllib2.urlopen(submission_URL).read()
        soup = BeautifulSoup(page, 'html.parser')
        saveDescription(soup, folder_title + '/' + chapter_name)
        saveFiles(soup, folder_title + '/' + chapter_name)


def checkFolder(folder_title):
    if not os.path.exists(folder_title):
        os.makedirs(folder_title)


def makeFolder(folder_title):
    if not os.path.exists(folder_title):
        os.makedirs(folder_title)
    else:
        print("This Chapter's folder already exists: " + folder_title)


def saveDescription(page, folder_title):
    description = page.select('div div p')[0].encode_contents()
    text_file = open(folder_title + "/description.txt", "w")
    text_file.write(description)
    text_file.close()


def saveFiles(page, folder_title):
    file_URL_list = page.select('div div ul li a')
    # Get rid of FB and email links in footer
    file_URL_list = file_URL_list[:-2]
    for file_URL in file_URL_list:
        file_URL = file_URL['href']
        file_URL = 'http://www.deltau.org' + str(file_URL)

        remotefile=urllib2.urlopen(file_URL)
        try:
            filename=remotefile.info()['Content-Disposition'][22:-1]
        except KeyError:
            print('=== KeyError ===\n\n')
            filename=os.path.basename(urllib2.urlparse.urlsplit(file_URL).path)
        urllib.urlretrieve(file_URL, folder_title + '/' +  filename)


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
