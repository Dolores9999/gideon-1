
import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import urllib.request
import json
from bs4 import BeautifulSoup as soup
import wikipedia
import random
from time import strftime
from pygame import mixer
import pygame
import multiprocessing
import time
from threading import Thread



class Gideon():
    def __init__(self, *args, **kwargs):
        self.password=''


    # to do  - implement a password system, fix the lookup function, connect it to a front end
    #
    def create_thread(self):
        p2 = Thread(target=self.play_song)
        p2.stop()

    def gideonResponse(self,audio):
        print(audio)
        for line in audio.splitlines():
            os.system("say " + line)


    def play_song(self):
        song1='/Users/mihailbratanov/Top Tracks - The Pretty Reckless/18 - The Pretty Reckless - Sweet Things (audio).mp3'
        song='/Users/mihailbratanov/BabyMetal - Karate (Kan_Rom_Eng Lyrics) (320 kbps).mp3'
        self.gideonResponse('Time to wake up you sleeping bitch!')
        time.sleep(1)
        mixer.init()
        mixer.music.load(song)
        mixer.music.play(-1)

    def wake_me_up(self):

        while True:
            day_time_hours = strftime('%H')
            day_time_minutes = strftime('%M')
            day_time_seconds = strftime('%S')


            if day_time_hours=="08" and day_time_minutes=="00"  and int(day_time_seconds)==2 :
                self.play_song()


    def myCommand(self):

        r=sr.Recognizer()
        with sr.Microphone() as src:
            #r.pause_threshold =1
            # r.adjust_for_ambient_noise(src, duration=0.5)
            audio = r.listen(src)
        try:
            command = r.recognize_google(audio).lower()
            print("You said: " + command)
            #here we need to loop back in case unrecognized speech is received
        except sr.UnknownValueError:
            print('......')
            # self.gideonResponse("Sorry sir, I did not catch that. Could you please say it again?")
            command = self.myCommand()
        return command

    def start_interface(self):
        while True:
            self.assistant(self.myCommand())


    def assistant(self, command):

        if "hello" in command:
            day_time = int(strftime('%H'))
            if day_time < 12:
                self.gideonResponse('Hello Sir. Good morning')
            elif 12 <= day_time < 18:
                self.gideonResponse('Hello Sir. Good afternoon')
            else:
                self.gideonResponse('Hello Sir. Good evening')

        elif "shut down" in command:
            self.gideonResponse('Goodbye Sir. Have a nice day.')
            sys.exit()

        elif "news" in command:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urllib.request.urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"html.parser")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    self.gideonResponse(news.title.text)
            except Exception as e:
                    print(e)
        elif "weather" in command:
            reg_ex = re.search('current weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                owm = OWM(api_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
                manager = owm.weather_manager()
                obs = manager.weather_at_place(city)
                w = obs.weather
                k = w.status
                x = w.temperature('celsius')['temp']
                self.gideonResponse("Current weather in %s is %s. The temparature is %s degrees Celsius." % (city, k,x))

        #time
        elif "time" in command:
            import datetime
            now = datetime.datetime.now()
            self.gideonResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

        elif "open" in command:
            reg_ex = re.search('open (.*)', command)
            if reg_ex:
                appname = reg_ex.group(1)
                appname = appname.capitalize()
                appname1 = appname+".app"
                subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
                self.gideonResponse('I have launched the desired application')
        # elif "search" in command:
        #     reg_ex = re.search('tell me about (.*)', command)
        #     try:
        #         if reg_ex:
        #             topic = reg_ex.group(1)
        #
        #             ny = wikipedia.summary(topic,sentences =2)
        #             self.gideonResponse(ny)
        #     except Exception as e:
        #             print(e)


if __name__ == '__main__':
    g=Gideon()
    p1 = multiprocessing.Process(name='p1', target=g.wake_me_up)
    p = multiprocessing.Process(name='p', target=g.start_interface)
    p1.start()
    p.start()

    # while True:
    #
    #     g.assistant(g.myCommand())

    # gideonResponse('Hi User, I am Gideon and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what I can do for you.')
