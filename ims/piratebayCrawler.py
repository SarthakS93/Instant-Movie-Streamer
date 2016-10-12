'''
PirateBay crawler
work of by SarthakS93
'''

import os, sys, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = 'https://piratebays.co.uk/'

def get_input():
    try:
        name = ' '.join(sys.argv[1 : ])
        name = name.lower()
        return name
    except:
        print('Invalid input')


def match(text, words):
    ctr = 0
    text = text.lower()
    for word in words:
        if word in text:
            ctr += 1
    print('Matching', ctr, words, text)
    if ctr >= len(words) - 1:
        return True
    else:
        return False


def get_page_link(name):
    try:
        print('getting page link')
        url = base_url + 's/'
        data = {'q': name, 'video': 'on', 'page': 0, 'orderby': 99}
        r = requests.get(url, params = data)
        print(r.status_code, r.url)
        soup = BeautifulSoup(r.text, 'lxml')

        searchBody = soup.find(id = 'searchResult')
        rows = searchBody.find_all('tr')[1 : ]
        if len(rows) > 0:
            words = name.split(' ')
            print(words)
            for r in rows:
                div = r.find_all('td')[1]
                a_tags = div.find_all('a')
                title = a_tags[0].text
                if match(title, words):
                    link = a_tags[1].get('href')
                    page_link = urljoin(base_url, link)
                    print(page_link)
                    return page_link
    except:
        print('Error in get_page_link')
        return None


def get_magnet_link(link):
    try:
        print('getting magnet link')
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'lxml')
        div = soup.find(class_ = 'download')
        a_tag = div.find('a')
        magnet_link = a_tag.get('href')
        return magnet_link
    except:
        print('Error in get_magnet_link')
        return None


def main():
    print('Starting the process')

    name = get_input()
    if not name:
        return

    link = get_page_link(name)
    if not link:
        return

    magnet_link = get_magnet_link(link)
    print(magnet_link)

    if magnet_link:
        os.system('peerflix "' + magnet_link + '" -a --vlc')

    #exit()
    print('End')

main()
