from dataclasses import replace
from fileinput import filename
from re import T
from urllib import response
import eyed3
from bs4 import BeautifulSoup
import requests
import os

songInput = ""
terminated = 0
path = os.getcwd()
dir_list = os.listdir(path)
filenum = 0
files = []
songs = []
urls = []
lyrics = []


def get_files():
    for x in dir_list:
        if x.endswith(".mp3"):
            files.append(x)


def list_files():
    for x in files:
        print(str(files.index(x)) + " - " + x)


def select_files():
    userInput = [int(x) for x in input(
        "Enter songs by number (separated by commas): ").split(",")]
    songs.extend(userInput)


def listmp3():
    get_files()
    list_files()
    select_files()


def getUrl():
    for i in range(len(songs)):
        audiofile = eyed3.load(files[int(i)])
        artist = audiofile.tag.artist
        song = audiofile.tag.title + ""
        meta = artist + "-" + song
        urls.append("https://genius.com/" + meta.replace(" ", "-") + "-lyrics")


def getLyrics():
    for i in range(len(urls)):
        print(urls[int(i)])
        response = requests.get(urls[int(i)])
        html_doc = response.text
        soup = BeautifulSoup(html_doc, "lxml")
        lyric = soup.find(attrs={"data-lyrics-container": "true"})
        for br in lyric.find_all("br"):
            br.replace_with("\n")
        filename = str(files[i])
        lyricsfile = filename[:filename.rfind(".")]
        with open(lyricsfile+".txt", "a", encoding='utf-8') as f:
            f.write(lyric.text)


listmp3()
url = getUrl()
getLyrics()
