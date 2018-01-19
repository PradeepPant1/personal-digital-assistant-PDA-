import bluetooth
import sys
from time import sleep
import random
bd_addr = "98:D3:31:80:96:67"
port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
import requests
import feedparser
from bs4 import BeautifulSoup
import re
import webbrowser as w
from PyDictionary import PyDictionary
print 'Connected'
welcome=["Hello , how may i help you?","Good to see you","Pleased to meet you","hello  , what do you want me to do ?"]
def speak(arg):
    import os
    str="google_speech -l en '"+arg+"' -e speed 1"
    os.system(str)
def wakeup():
    import speech_recognition as sr
    while(1):
        r = sr.Recognizer()
        r.energy_threshold = 4000
        r.pause_threshold = 0.5
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
         
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            strt=r.recognize_google(audio)
        #strt.lower()
       # print(strt)
            if(strt=="hi Alex"):
                print("You said: " + strt)
                speak("Hello , Rishabh how may i help you")
                return 1
            else:
                speak("I am not in a mood")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
def weather(args):
    import pyowm
    #.........preprocessing
    args=args.lower()
    #print args
    l=args.split(" ")
    #print l
    length=len(l)
    try:
        i=l.index('city')
        city=l[i+1:length]
        city=' '.join(city)
        print city
        #..............
        owm = pyowm.OWM('3a717ad44622a5f1826626611d8e736d')
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        #print(w.get_temperature('celsius'))
        temp=(w.get_temperature('celsius')).get('temp')
        print temp
        speak("Weather in "+city+" is "+str(temp)+" degree celcius")
    except ValueError:
        print ("Speak city")
        speak ("Please Speak City before city name")

def playSong(args):
    try:
        if(args.find("gaana")!=-1 or args.find("gana")!=-1):
            print(args)
            page = requests.get("http://www.google.com/search?hl=en&q=" +args)
            soup = BeautifulSoup(page.text,"lxml")
            link=soup.find("a",href=re.compile("(?<=/url\?q=)(htt.*://gaana.com/song.*)"))
            t=re.split(":(?=http)",link["href"].replace("/url?q=",""))
            w.open(t[0])
        else:
            page = requests.get("http://www.google.com/search?hl=en&q="+ args)
            soup = BeautifulSoup(page.text,"lxml")
            link=soup.find("a",href=re.compile("(?<=/url\?q=)(htt.*://www.youtube.com.*)"))
            t=re.split(":(?=http)",link["href"].replace("/url?q=",""))
            str=t[0].replace("%3F","?")
            str=str.replace("%3D","=")
            str=re.sub("&sa=.*$","",str)
            print str
            w.open(str,)
    except:
        print ("invalid input")
        speak ("Sorry, i did not understand what you said?")
def getNewsHeadlines(  ):
    headlines = []
    #url="http://news.google.com/?output=rss"
    url="https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"
    feed = feedparser.parse(url) 
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines
if __name__ == "__main__":
    import speech_recognition as sr
    import os
    import re
    if(wakeup()==1):
        while(1):
            r = sr.Recognizer()
            r.energy_threshold = 4000
            r.pause_threshold = 0.5
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            # Speech recognition using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                said=r.recognize_google(audio)
                print("You said: " + said)
            #said.lower()
                dictionary=PyDictionary()
                if(re.search("meaning.*$",said)):
                    a=re.search("for.*$|of.*$",said)
                    try:
                        word=a.group()[3:len(a.group())]
                        temp=dictionary.meaning(word).values()[0][0]
                        temp=word +" is. "+temp
                        speak (temp)
                    except:
                        print ("invalid input")
                        speak ("Sorry, i did not understand what you said?")
                if(re.search("synonym.*$",said)):
                    try:
                        a=re.search("for.*$|of.*$",said)
                        word=a.group()[3:len(a.group())]
                        temp=dictionary.synonym(word)[0]
                        temp="Synonym of "+word +" is. "+temp
                        speak (temp)
                    except:
                        print ("invalid input")
                        speak ("Sorry, i did not understand what you said?")
                if(re.search("antonym.*$",said)):
                    try:
                        a=re.search("for.*$|of.*$",said)
                        word=a.group()[3:len(a.group())]
                        temp=dictionary.antonym(word)[0]
                        temp="Antonym of "+word +" is. "+temp
                        speak (temp)
                    except:
                        print ("invalid input")
                        speak ("Sorry, i did not understand what you said?")
                if(re.search("(?i)^news.*$",said)):
                    try:
                        allheadlines = []
                        news=[]
                        flag=False
                        allheadlines.extend(getNewsHeadlines()) 
                        for hl in allheadlines:
                            news.append(str(hl))
                        new=news[1:3]
                        for i in new:
                            if flag == True:
                                speak(i)
                            flag=True
                    except:
                        print ("invalid input")
                        speak ("Sorry, i did not understand what you said?")
                if(said.search("stop")):
                    try:
                        os.system("killall -KILL chromium-browser")
                    except:
                        print ("invalid input")
                        speak ("no song is playing right now")
                if(said.find("weather")!=-1):
                    weather(said)
                if(re.search("(?i)^play.*song.*$|^play.*music.*$|^play.*$",said)):
                    playSong(str(said))
                    speak("PLAYING MUSIC BE PATIENT.!")
                if(re.search('(?i)on',said) and re.search('(?i)light',said) ):
                    try:
                        send="Lights on"
                        sock.send(send)
                        speak("Ok Turning on the lights!")
                    except:
                        print ("bluetooth connectivity")
                        speak ("it seems your bluetooth is not connected...")
                if(re.search('(?i)call',said)):
                    try:
                        a=re.search("[0-9].*$",said)
                        ab=a.group().replace(" ","")
                        if(len(str(ab))==10):
                            send="Call"
                            sock.send(send)
                            speak("Ok calling")
                            print ab
                            sock.send(ab)
                        else:
                            print ("number not correct")
                            speak ("The contact number you dialed is not correct")
                    except:
                        print ("connectivity issues")
                        speak ("check ur connections")
                    
                if(re.search('(?i)off',said) and re.search('(?i)light',said) ):
                    try:
                        send="Lights off"
                        sock.send(send)
                        speak("Ok Turning off the lights!")
                    except:
                        print ("bluetooth connectivity")
                        speak ("it seems your bluetooth is not connected...")
                if(said=="hi Alex"):
                    speak(random.choice(welcome))
                    #print(ser.readline())
                sock.send("");
                said=""
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))


