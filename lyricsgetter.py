from dataclasses import replace
from fileinput import filename
from re import T
from urllib import response
import eyed3
from bs4 import BeautifulSoup
import requests
import os

songInput = ""


def getUrl():
    audiofile = eyed3.load(songInput+".mp3")
    artist = audiofile.tag.artist
    song = audiofile.tag.title + ""
    meta = artist + "-" + song
    return "https://genius.com/" + meta.replace(" ", "-") + "-lyrics"


def checkForLyricsFile():
    if os.path.exists(songInput):
        print("Lyrics already exist")
        user = input("Would you like to override them? (y/n) ")
        if user == "y":
            os.remove(songInput)


def getLyrics(url):
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "lxml")
    lyrics = soup.find(attrs={"data-lyrics-container": "true"})
    for br in lyrics.find_all("br"):
        br.replace_with("\n")
    return lyrics.text


def writeLyricsToFile(lyrics):
    song = songInput+".txt"
    with open(songInput+".txt", "a", encoding='utf-8') as f:
        f.write(lyrics)


while True:
    songInput = input(
        "Type in the filename of the song you want lyrics for: ")
    song = songInput + ".mp3"
    if not os.path.exists(songInput+".mp3"):
        print("That file does not exist. Check the name for typos.")
    else:
        break
url = getUrl()
checkForLyricsFile()
writeLyricsToFile(getLyrics(url))

print("Lyrics file created")
