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
class Gideon():
    def __init__(self, *args, **kwargs):
        self.password=''

    # to do  - implement a password system, fix the lookup function, connect it to a front end 
    # 
    def gideonResponse(self,audio):
        print(audio)
        for line in audio.splitlines():
            os.system("say " + line)

    def myCommand(self):
        r=sr.Recognizer()
        with sr.Microphone() as src:
            print("Say something")
            # r.pause_threshold =1 
            r.adjust_for_ambient_noise(src, duration=0.5)
            audio = r.listen(src)
        try: 
            command = r.recognize_google(audio).lower()
            print("You said: " + command + '\n')
            #here we need to loop back in case unrecognized speech is received 
        except sr.UnknownValueError:
            print('......')
            self.gideonResponse("Sorry sir, I did not catch that. Could you please say it again?")
            command = self.myCommand()
        return command

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
        
        elif "news for today" in command:
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
        elif "current weather" in command:
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
        elif "tell me about" in command:
            reg_ex = re.search('tell me about (.*)', command)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    
                    ny = wikipedia.summary(topic,sentences =2)
                    self.gideonResponse(ny)
            except Exception as e:
                    print(e)
                    self.gideonResponse(e)

if __name__ == '__main__':
    g=Gideon()
    while True:
        g.assistant(g.myCommand())

    # gideonResponse('Hi User, I am Gideon and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what I can do for you.')

