"""
YOU NEED TO DOWNLOAD:
gTTS for the text to speech,
PRAW 4.0.0b (<3 bboe)
"""
import praw
import time
from gtts import gTTS
import os
import random

#Please set the default mp3 player to Windows Media Player for this to work properly, but it may work otherwise

#CHANGE THESE
max_title_char = 70
url_space_amount = 5
post_limit = 10
file_path = "C:\\"
#Use Text-to-speech?
TextToSpeech = True


reddit = praw.Reddit(user_agent='Reddit RRS Feed u/BestLucarioFan', client_id='YOUR CLIENT ID HERE',
                  client_secret='YOUR CLIENT SECRET HERE')


def speak_text(spoken_text):
    file_counter = random.randrange(1,10000)
    save_path = file_path+"text"+str(file_counter)+".mp3"
    tts = gTTS(text=spoken_text, lang='en')
    #Saves mp3 file to specified path
    tts.save(save_path)
    #Starts mp3 file minimised, doesn't always minimise :(
    os.system("start /min " + save_path)
    time.sleep(9)
    #Only on certain mp3 players
    #os.system("taskkill /f /im  vmplayer.exe")
    time.sleep(1)
    #Deletes file
    os.remove(save_path)


def shortenTitles(title, max_length=max_title_char):
    #If the title is more than the specified amount of characters long, shorten it with ...
    if len(title) > max_length:
        return title[:max_length - 3] + "..."
    else:
        return title

#List to store already displayed posts
displayedTitles = []

#Asks for subreddit info
chosen_subreddit = input("What subreddit to browse:  ")
subreddit = reddit.subreddit(chosen_subreddit)

print("r/"+chosen_subreddit+":")


def fetchTitles():

    for post in subreddit.new(limit=post_limit):

        printAmount = 0

        post_length = len(post.title)
        post_title = str(post.title)
        wasShown = False
        for sent in displayedTitles:
            if sent == post_title:
                wasShown = True
        #If it is not in the displayedTitles List
        if wasShown is False:
            if TextToSpeech:
                speak_text(post_title)
            displayedTitles[:0] = [post_title]
            post_title = shortenTitles(post_title)
            post_length = len(post_title)

            #Determine the amount of spaces needed
            max_title_space_char = max_title_char + url_space_amount
            space_amount = max_title_space_char - post_length
            print("\t" + str(post_title) + space_amount * (" ") + post.url)
            printAmount += 1
    return printAmount

counter = 0
while True:
    #Optimisation... When the amount of posts in the displayedTitles is 2x the post_limit, it deletes the old ones
    while counter <= post_limit + post_limit:
        counter = fetchTitles()
        time.sleep(10)
    displayedTitles[post_limit:] = []
    counter = 0

