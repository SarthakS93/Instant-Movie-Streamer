'''
PirateBay crawler
work of by SarthakS93
'''

import os, sys, requests
from bs4 import BeautifulSoup

url = 'https://piratebays.co.uk/s/'

def get_input():
    try:
        name = ' '.join(sys.argv[1 : ])
        return name
    except:
        print('Invalid input')


def get_request_object(name):
    try:
        data = {'q': name, 'video': 'on', 'page': 0, 'orderby': 99}
        r = requests.get(url, params = data)
        return r
    except:
        print('Error while connecting')



def get_soup_object(request_obj):
    try:
        print(request_obj.url)
        soup = BeautifulSoup(request_obj.text, 'lxml')
        return soup
    except:
        print('Error while preparing soup object')


def get_magnet_link(soup):
    try:
        print(soup.title)
        print(len(soup.find_all('a')))
    except:
        return None



def main():
    print('Starting the process')

    name = get_input()
    if not name:
        return

    request_obj = get_request_object(name)
    if not request_obj:
        return

    soup = get_soup_object(request_obj)
    if not soup:
        return

    link = get_magnet_link(soup)
    if not link:
        return

    print('End')

main()
