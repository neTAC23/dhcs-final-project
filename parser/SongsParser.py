import urllib2
import cookielib
import bs4 as bs
import os
import json
import io


class Song:
    def __init__(self, url, title, year, singer, lyrics):
        self.url = url
        self.title = title
        self.year = year
        self.singer = singer
        self.lyrics = lyrics


def opener():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
                    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'),
                    ('Connection', 'keep-alive'),
                ]
    urllib2.install_opener(opener)
    return opener


def parse_song(url, i, artist):
    my_opener = opener()
    my_opener.open(url, timeout=30)
    resp = my_opener.open(url)
    soup = bs.BeautifulSoup(resp, 'html.parser')
    if soup.h1:
        title = soup.h1.string + "_" + str(i)
        title = title.replace("/", "").replace("\\", "").replace("\"", "").replace("*", "").replace(":", "")
        title = title.replace("?", "").replace("<", "").replace(">", "").replace("|", "")
        singer = soup.find(class_="artist_singer_title").string if soup.find(class_="artist_singer_title") else artist
        singer = singer.replace("/", "").replace("\\", "").replace("\"", "").replace("*", "").replace(":", "")
        singer = singer.replace("?", "").replace("<", "").replace(">", "").replace("|", "")
        year = soup.find(class_="artist_color_gray").string if soup.find(class_="artist_color_gray") else 0
        lyrics = soup.find(class_="artist_lyrics_text").text
        print(singer)
        print(title)
        song = Song(url, title, year, singer, lyrics)
        songs.append(song)
        data['songs'].append({
            'url': url,
            'title': title,
            'year': year,
            'singer': singer,
        })
    else:
        parse_song(url, i, artist)


def parse_artists_songs(url, i, prev_page, artist):
    my_opener = opener()
    my_opener.open(url, timeout=30)
    resp = my_opener.open(url)
    soup = bs.BeautifulSoup(resp, 'html.parser')
    # table width="100%" border="0" cellspacing="3" cellpadding="0" dir="rtl" style="padding-right: 5px"
    songs_table = soup.find("table", {'width': '100%', 'cellspacing': '3', 'cellpadding': '0'})
    if songs_table:
        songs = songs_table.findAll(class_="artist_player_songlist")
        for song in songs:
            print(str(i) + ': https://shironet.mako.co.il'+song.get("href"))
            i += 1
            parse_song('https://shironet.mako.co.il'+song.get("href"), i, artist)

    pages = soup.findAll(class_="artist_nav_bar")
    if pages:
        next_page = 'https://shironet.mako.co.il'+pages[pages.__len__()-1].get("href")
        print(next_page)
        print(url)
        print(prev_page)
        if prev_page and prev_page.split("page=").__len__() > 1:  # parser is in the third page or more
            prev_page = prev_page.split("page=")[1]
            next = next_page.split("page=")[1]
            print(int(next), int(prev_page))
            if int(next) > int(prev_page):
                parse_artists_songs(next_page, i, url, artist)
        else:
            if next_page != prev_page and int(next_page.split("page=")[1]) > 1:
                parse_artists_songs(next_page, i, url, artist)


def parse_artists(url, prev_page):
    my_opener = opener()
    my_opener.open(url, timeout=30)
    resp = my_opener.open(url)
    soup = bs.BeautifulSoup(resp, 'html.parser')
    artists = soup.findAll(class_="index_link")
    for artist in artists:
        artist_url = 'https://shironet.mako.co.il/artist?type=works&'+artist.get("href")[8:]
        artist_name = artist.string.strip()
        parse_artists_songs(artist_url, 0, "", artist_name)
    pages = soup.findAll(class_="index_nav_bar")
    if pages:
        next_page = 'https://shironet.mako.co.il'+pages[pages.__len__()-1].get("href")
        if prev_page and prev_page.split("page=").__len__()>1:
            prev_page = prev_page.split("page=")[1]
            next = next_page.split("page=")[1]
            if int(next) > int(prev_page):
                parse_artists(next_page, url)
        else:
            if next_page != prev_page and int(next_page.split("page=")[1]) > 1:
                parse_artists(next_page, url)


def write_lyrics_and_metadata(lyrics_dir):
    for song in songs:
        file_name = song.singer+"_"+song.title+".txt"
        filepath = os.path.join(lyrics_dir, file_name)
        with io.open(filepath, 'w+', encoding='utf8') as file:
            file.write(song.lyrics)


def read_page(url):
    my_opener = opener()
    my_opener.open(url, timeout=30)
    resp = my_opener.open(url)
    soup = bs.BeautifulSoup(resp, 'html.parser')
    with io.open("bible_html.txt", 'w+', encoding='utf8') as outfile:
        outfile.write(soup.prettify())


data = {}
data['songs'] = []
songs = []
lyrics_dir = "D:/bgu/dhcs/lyrics_8"
url = "https://shironet.mako.co.il/html/indexes/performers/heb_8_alpha.html"
parse_artists(url, "")
write_lyrics_and_metadata(lyrics_dir)
lyrics_data = "D:/bgu/dhcs/lyrics_data_8.txt"
with io.open(lyrics_data, 'w+', encoding='utf8') as outfile:
    outfile.write(unicode(json.dumps(data, ensure_ascii=False)))

