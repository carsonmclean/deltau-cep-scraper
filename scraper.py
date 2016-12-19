from bs4 import BeautifulSoup
import urllib2


def getCEPMainPage():
    url = 'http://www.deltau.org/ChapterExcellence'
    return urllib2.urlopen('http://www.deltau.org/ChapterExcellence').read()

def makeSoup(page):
    return BeautifulSoup(page, 'html.parser')

def main():
    CEPMainPage = getCEPMainPage()
    soup = makeSoup(CEPMainPage)
    print(soup.prettify())

if __name__ == '__main__':
    main()
else:
    print("This program should be run directly!")
