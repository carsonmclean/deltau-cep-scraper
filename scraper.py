from bs4 import BeautifulSoup
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

def main():
    chapter_URLs = getChapterURLs()


if __name__ == '__main__':
    main()
else:
    print("This program should be run directly!")
