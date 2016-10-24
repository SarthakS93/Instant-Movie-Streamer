#!/usr/bin/env python

import os
import sys

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
DEBUG = False


def test_system():
    """Runs few tests to check if npm and peerflix is installed on the system."""
    if os.system('npm --version') != 0:
        print 'NPM not installed installed, please read the Readme file for more information.'
        exit()
    if os.system('peerflix --version') != 0:
        print 'Peerflix not installed, installing..'
        os.system('npm install -g peerflix')


def get_input():
    """Gets the input from user and formats it."""
    try:
        query = ' '.join(sys.argv[1:])
        cat = query.split()[0]
        movie_name = ' '.join(query.split()[1:])
        if cat == 'movie':
            query = (movie_name + ' category:movies').replace(' ', '%20')
        elif cat == 'tv':
            query = (movie_name + ' category:tv').replace(' ', '%20')
        else:
            print 'Invalid format, please specify if its a movie or tv series.'
            exit()
    except Exception as e:
        print e
        exit()
    return query


def get_torrent_url(search_url):
    """Grabs the best matched torrent URL from the search results."""
    search_request_response = requests.get(search_url, verify=False)
    soup = BeautifulSoup(search_request_response.text, 'html.parser')
    movie_page = 'https://kat.cr' + (soup.find_all("a", class_="cellMainLink")[0].get('href'))

    search_url = requests.get(movie_page, verify=False)
    soup = BeautifulSoup(search_url.text, 'html.parser')
    torrent_url = 'https:' + soup.find_all('a', class_='siteButton')[0].get('href')
    return torrent_url


base_url = 'https://piratebays.co.uk/'

def match(text, words):
    ctr = 0
    text = text.lower()
    for word in words:
        if word in text:
            ctr += 1
    if ctr >= len(words) - 1:
        return True
    else:
        return False


def get_page_link(name):
    try:
        url = base_url + 's/'
        data = {'q': name, 'video': 'on', 'page': 0, 'orderby': 99}
        r = requests.get(url, params = data)
        soup = BeautifulSoup(r.text, 'html.parser')

        searchBody = soup.find(id = 'searchResult')
        rows = searchBody.find_all('tr')[1 : ]
        if len(rows) > 0:
            words = name.split(' ')
            for r in rows:
                div = r.find_all('td')[1]
                a_tags = div.find_all('a')
                title = a_tags[0].text
                if match(title, words):
                    link = a_tags[1].get('href')
                    page_link = urljoin(base_url, link)
                    return page_link
    except Exception as e:
        print e
        return None


def get_magnet_link(link):
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find(class_ = 'download')
        a_tag = div.find('a')
        magnet_link = a_tag.get('href')
        return magnet_link
    except Exception as e:
        print e
        return None


test_system()
movie = get_input()
url = 'http://dx-torrente.com/usearch/' + movie
if DEBUG:
    print url
torrent_url = ''
try:
    print 'Searching....'
    torrent_url = get_torrent_url(url)
except Exception as e:
    #print e
    print 'Taking a bit longer....Please wait..'
    movie_name = ' '.join(sys.argv[2 : ])
    name = movie_name.lower()
    link = get_page_link(name)
    if link:
        torrent_url = get_magnet_link(link)
    if torrent_url == '':
        exit()

if torrent_url:
    print ('Streaming Torrent: ' + torrent_url)
    os.system('peerflix ' + torrent_url + ' -a --vlc')
else:
    print 'No results found'
