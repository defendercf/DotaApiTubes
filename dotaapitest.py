import os
import re
import threading
import time
import tkinter as tk
from distutils.errors import UnknownFileError
from io import BytesIO
from tkinter import ttk

import pyttsx3
import requests as req
import speech_recognition as sr
import steamid_converter.Converter as Converter
from gtts import gTTS
from PIL import Image, ImageTk

api_key = "bca71228-5abf-4825-8ff5-ea2ce7afb60e"

def remove(string):
    return string.replace(" ", "")

def say(text1):
     language = 'en'
     speech = gTTS(text = text1, lang = language, slow = False)
     speech.save("text.mp3")
     os.system("start text.mp3")

def clear_frame():
   for widgets in entry_frame.winfo_children():
      widgets.destroy()

def talk(text1):
  engine = pyttsx3.init()
  voice = engine.getProperty('voices')
  engine.setProperty('voice', voice[1].id)
  engine.setProperty('rate', 150)
  engine.say(text1)
  engine.runAndWait()
  
def speechrecogID():
  try:
    while True:
      r = sr.Recognizer()
      with sr.Microphone() as source:
        # read the audio data from the default microphone
        label1.config(text="")
        label1.config(text="Please talk")
        talk("Please Say your ID in 3 second")
        audio_data = r.record(source, duration=8)
        talk("Time up")
        label1.config(text="")
        label1.config(text="Time Up")
        # audio_data = r.listen(source)
        label1.config(text="")
        label1.config(text="Recognizing Voice....")
        text = r.recognize_google(audio_data)
        text = text.lower()
        text = re.sub(r'[^0-9]', '', text)
        text = remove(text)
        talk(f"Are you saying {text}")
        print(text)
        label1.config(text="")
        label1.config(text=f"Are you saying {text}")
        talk("Please confirm your text with yes or no in 2 second")
        audio_data = r.record(source, duration=3)
        label1.config(text="")
        label1.config(text="Recognizing Voice....")
        text2 = r.recognize_google(audio_data)
        text2 = text2.lower()
        print(text)
        if "yes" in text2:
          text = remove(text)
          talk(f"You are saying {text}")
          label1.config(text="")
          label1.config(text=f"You are saying {text}")
          return text
        elif "no" in text2:
          label1.config(text="Repeating!")
          talk("Repeating")
          continue
  except sr.UnknownValueError:
    label1.config(text="")
    label1.config(text="Error Has Occured")
    talk("Error Has Occured")
        
def speechrecog():
  try:
    while True:
      r = sr.Recognizer()
      with sr.Microphone() as source:
        # read the audio data from the default microphone
        label1.config(text="Please talk")
        talk("Please Start Talking in 3 second")
        audio_data = r.record(source, duration=6)
        label1.config(text="Recognizing Voice....")
        text = r.recognize_google(audio_data)
        text = text.lower()
        print(text)
        talk(f"Are you saying {text}")
        label1.config(text="-")
        talk("Please confirm your text with yes or no in 2 second")
        audio_data = r.record(source, duration=3)
        label1.config(text="Recognizing Voice....")
        text2 = r.recognize_google(audio_data)
        text2 = text2.lower()
        if "yes" in text2:
          talk(f"You are saying {text}")
          label1.config(text=f"You are saying {text}")
          return text
          break
        elif "no" in text2:
          label1.config(text="Repeating!")
          talk("Repeating")
          continue
  except:
    label1.config(text="")
    label1.config(text="Error Has Occured")
    talk("Error Has Occured")

def accessID():
  clear_frame()
  idinput = entry1.get()
  id_api_url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=A2BE1B4A3BBC3A62B72C6096216AA9F9&vanityurl={idinput}"
  respid = req.get(id_api_url)
  print(respid.status_code)
  id_json_data = respid.json()
  print(id_json_data)
  steamid64 = id_json_data['response']['steamid']
  steamid3 = str(Converter.to_steamID3(steamid64))
  steamid3 = steamid3[5:14]
  print(steamid3)
  
  api_url = f"https://api.opendota.com/api/players/{steamid3}?api_key=bca71228-5abf-4825-8ff5-ea2ce7afb60e"
  print(api_url)
  resp = req.get(api_url)
  print(resp.status_code)
  json_data = resp.json()
  print(json_data)
  
  api_url2 = f"https://api.opendota.com/api/players/{steamid3}/wl"
  print(api_url2)
  resp2 = req.get(api_url2)
  print(resp2.status_code)
  json_data2 = resp2.json()
  print(json_data2)
  winrate = ""
  win = json_data2["win"]
  lose = json_data2["lose"]
  if win == 0 or lose == 0:
    winrate = "N/A"
  else:
    total = win + lose
    winrate = (win/total)*100
    winrate = f"{round(winrate,2)} %"
    winrate = f"{winrate}\n{win}/{total} games"
  
  img_url = json_data['profile']['avatarfull']
  response = req.get(img_url)
  img_data1 = response.content
  img1 = ImageTk.PhotoImage(Image.open(BytesIO(img_data1)))


    # Username Entry
  photo1 = ttk.Label(entry_frame, image=img1)
  photo1.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)
  nicknamedata = json_data['profile']['personaname']
  nickname = ttk.Label(entry_frame,text=f"Nick :\n{nicknamedata}")
  nickname.grid(row=0,column=1,padx=5,pady=5)
  ranktier= json_data['rank_tier']
  if ranktier == None:
    ingameRank = "Unranked"
    rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e7/SeasonalRank0-0.png/revision/latest/scale-to-width-down/230?cb=20171124184310"
  else:
    firstLT = int(str(ranktier)[0])
    secondLT = int(str(ranktier)[1])
    print(firstLT,secondLT)
    if firstLT == 1:
      ingameRank = "Herald "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/85/SeasonalRank1-1.png/revision/latest/scale-to-width-down/160?cb=20190130002445"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/ee/SeasonalRank1-2.png/revision/latest/scale-to-width-down/160?cb=20190130002448"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/0/05/SeasonalRank1-3.png/revision/latest/scale-to-width-down/160?cb=20190130002457"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6d/SeasonalRank1-4.png/revision/latest/scale-to-width-down/160?cb=20190130002500"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2b/SeasonalRank1-5.png/revision/latest/scale-to-width-down/160?cb=20190130002504"
    elif firstLT == 2:
      ingameRank = "Guardian "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c7/SeasonalRank2-1.png/revision/latest/scale-to-width-down/160?cb=20190130002542"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2c/SeasonalRank2-2.png/revision/latest/scale-to-width-down/160?cb=20190130002545"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f5/SeasonalRank2-3.png/revision/latest/scale-to-width-down/160?cb=20190130002548"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/b4/SeasonalRank2-4.png/revision/latest/scale-to-width-down/160?cb=20190130002552"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/32/SeasonalRank2-5.png/revision/latest/scale-to-width-down/160?cb=20190130002555"
    elif firstLT == 3:
      ingameRank = "Crusader "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/82/SeasonalRank3-1.png/revision/latest/scale-to-width-down/160?cb=20190130002626"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/SeasonalRank3-2.png/revision/latest/scale-to-width-down/160?cb=20190130002629"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/67/SeasonalRank3-3.png/revision/latest/scale-to-width-down/160?cb=20190130002632"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/87/SeasonalRank3-4.png/revision/latest/scale-to-width-down/160?cb=20190130002635"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = ""
    elif firstLT == 4:
      ingameRank = "Archon "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/76/SeasonalRank4-1.png/revision/latest/scale-to-width-down/160?cb=20190130002704"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/87/SeasonalRank4-2.png/revision/latest/scale-to-width-down/160?cb=20190130002707"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/60/SeasonalRank4-3.png/revision/latest/scale-to-width-down/160?cb=20190130002710"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/4a/SeasonalRank4-4.png/revision/latest/scale-to-width-down/160?cb=20190130002714"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a3/SeasonalRank4-5.png/revision/latest/scale-to-width-down/160?cb=20190130002718"
    elif firstLT == 5:
      ingameRank = "Legend "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/79/SeasonalRank5-1.png/revision/latest/scale-to-width-down/160?cb=20190130002757"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/52/SeasonalRank5-2.png/revision/latest/scale-to-width-down/160?cb=20190130002839"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/88/SeasonalRank5-3.png/revision/latest/scale-to-width-down/160?cb=20190130002819"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/25/SeasonalRank5-4.png/revision/latest/scale-to-width-down/160?cb=20190130002822"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8e/SeasonalRank5-5.png/revision/latest/scale-to-width-down/160?cb=20190130002826"
    elif firstLT == 6:
      ingameRank = "Ancient "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e0/SeasonalRank6-1.png/revision/latest/scale-to-width-down/160?cb=20190130002941"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/1c/SeasonalRank6-2.png/revision/latest/scale-to-width-down/160?cb=20190130002945"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/da/SeasonalRank6-3.png/revision/latest/scale-to-width-down/160?cb=20190130002948"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/db/SeasonalRank6-4.png/revision/latest/scale-to-width-down/160?cb=20190130002951"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/47/SeasonalRank6-5.png/revision/latest/scale-to-width-down/160?cb=20190130002955"
    elif firstLT == 7:
      ingameRank = "Divine "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/b7/SeasonalRank7-1.png/revision/latest/scale-to-width-down/160?cb=20190130003022"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8f/SeasonalRank7-2.png/revision/latest/scale-to-width-down/160?cb=20190130003026"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/fd/SeasonalRank7-3.png/revision/latest/scale-to-width-down/160?cb=20190130003029"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/13/SeasonalRank7-4.png/revision/latest/scale-to-width-down/160?cb=20190130003033"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/33/SeasonalRank7-5.png/revision/latest/scale-to-width-down/160?cb=20190130003041"
    elif firstLT == 8:
      ingameRank = "Immortal"
      rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f2/SeasonalRankTop0.png/revision/latest/scale-to-width-down/160?cb=20180606220529"

  response = req.get(rankimgurl)
  img_data2 = response.content
  img2 = ImageTk.PhotoImage(Image.open(BytesIO(img_data2)))
  photo2 = ttk.Label(entry_frame, image=img2)
  photo2.grid(row=1,column=0,padx=5,pady=5,sticky=tk.W)
  rank = ttk.Label(entry_frame,text=f"Rank :\n{ingameRank}")
  rank.grid(row=1,column=1,padx=5,pady=5)
  winrate = ttk.Label(entry_frame, text=f"Winrate : {winrate}")
  winrate.grid(row=3,column=1,padx=5,pady=5)
  
  root.mainloop()

def accessIDviaSpeech():
  clear_frame()
  text = speechrecogID()
  print(text)
  idinput = ''
  idinput = text 
  print(idinput)
  if len(idinput) == 9:
    steamid3 = idinput
  else:
    id_api_url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=A2BE1B4A3BBC3A62B72C6096216AA9F9&vanityurl={idinput}"
    respid = req.get(id_api_url)
    print(respid.status_code)
    id_json_data = respid.json()
    print(id_json_data)
    steamid64 = id_json_data['response']['steamid']
    steamid3 = str(Converter.to_steamID3(steamid64))
    steamid3 = steamid3[5:14]
    print(steamid3)
  
  #API for profile
  api_url = f"https://api.opendota.com/api/players/{steamid3}?api_key=bca71228-5abf-4825-8ff5-ea2ce7afb60e"
  print(api_url)
  resp = req.get(api_url)
  print(resp.status_code)
  json_data = resp.json()
  print(json_data)
  
  #API for W/L
  api_url2 = f"https://api.opendota.com/api/players/{steamid3}/wl"
  print(api_url2)
  resp2 = req.get(api_url2)
  print(resp2.status_code)
  json_data2 = resp2.json()
  print(json_data2)
  winrate = ""
  win = json_data2["win"]
  lose = json_data2["lose"]
  if win == 0 or lose == 0:
    winrate = "N/A"
  else:
    total = win + lose
    winrate = (win/total)*100
    winrate = f"{round(winrate,2)} %"
    winratetotal = f"{winrate}\n{win}/{total} games"
  
  
  img_url = json_data['profile']['avatarfull']
  response = req.get(img_url)
  img_data1 = response.content
  img1 = ImageTk.PhotoImage(Image.open(BytesIO(img_data1)))

  photo1 = ttk.Label(entry_frame, image=img1)
  photo1.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)
  nicknamedata = json_data['profile']['personaname']
  nickname = ttk.Label(entry_frame,text=f"Nick :\n{nicknamedata}")
  nickname.grid(row=0,column=1,padx=5,pady=5)
  ranktier= json_data['rank_tier']
  if ranktier == None:
    ingameRank = "Unranked"
    rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e7/SeasonalRank0-0.png/revision/latest/scale-to-width-down/230?cb=20171124184310"
  else:
    firstLT = int(str(ranktier)[0])
    secondLT = int(str(ranktier)[1])
    print(firstLT,secondLT)
    if firstLT == 1:
      ingameRank = "Herald "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/85/SeasonalRank1-1.png/revision/latest/scale-to-width-down/160?cb=20190130002445"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/ee/SeasonalRank1-2.png/revision/latest/scale-to-width-down/160?cb=20190130002448"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/0/05/SeasonalRank1-3.png/revision/latest/scale-to-width-down/160?cb=20190130002457"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6d/SeasonalRank1-4.png/revision/latest/scale-to-width-down/160?cb=20190130002500"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2b/SeasonalRank1-5.png/revision/latest/scale-to-width-down/160?cb=20190130002504"
    elif firstLT == 2:
      ingameRank = "Guardian "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c7/SeasonalRank2-1.png/revision/latest/scale-to-width-down/160?cb=20190130002542"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2c/SeasonalRank2-2.png/revision/latest/scale-to-width-down/160?cb=20190130002545"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f5/SeasonalRank2-3.png/revision/latest/scale-to-width-down/160?cb=20190130002548"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/b4/SeasonalRank2-4.png/revision/latest/scale-to-width-down/160?cb=20190130002552"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/32/SeasonalRank2-5.png/revision/latest/scale-to-width-down/160?cb=20190130002555"
    elif firstLT == 3:
      ingameRank = "Crusader "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/82/SeasonalRank3-1.png/revision/latest/scale-to-width-down/160?cb=20190130002626"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6e/SeasonalRank3-2.png/revision/latest/scale-to-width-down/160?cb=20190130002629"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/67/SeasonalRank3-3.png/revision/latest/scale-to-width-down/160?cb=20190130002632"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/87/SeasonalRank3-4.png/revision/latest/scale-to-width-down/160?cb=20190130002635"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = ""
    elif firstLT == 4:
      ingameRank = "Archon "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/76/SeasonalRank4-1.png/revision/latest/scale-to-width-down/160?cb=20190130002704"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/87/SeasonalRank4-2.png/revision/latest/scale-to-width-down/160?cb=20190130002707"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/60/SeasonalRank4-3.png/revision/latest/scale-to-width-down/160?cb=20190130002710"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/4a/SeasonalRank4-4.png/revision/latest/scale-to-width-down/160?cb=20190130002714"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a3/SeasonalRank4-5.png/revision/latest/scale-to-width-down/160?cb=20190130002718"
    elif firstLT == 5:
      ingameRank = "Legend "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/79/SeasonalRank5-1.png/revision/latest/scale-to-width-down/160?cb=20190130002757"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/52/SeasonalRank5-2.png/revision/latest/scale-to-width-down/160?cb=20190130002839"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/88/SeasonalRank5-3.png/revision/latest/scale-to-width-down/160?cb=20190130002819"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/25/SeasonalRank5-4.png/revision/latest/scale-to-width-down/160?cb=20190130002822"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8e/SeasonalRank5-5.png/revision/latest/scale-to-width-down/160?cb=20190130002826"
    elif firstLT == 6:
      ingameRank = "Ancient "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e0/SeasonalRank6-1.png/revision/latest/scale-to-width-down/160?cb=20190130002941"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/1c/SeasonalRank6-2.png/revision/latest/scale-to-width-down/160?cb=20190130002945"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/da/SeasonalRank6-3.png/revision/latest/scale-to-width-down/160?cb=20190130002948"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/db/SeasonalRank6-4.png/revision/latest/scale-to-width-down/160?cb=20190130002951"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/47/SeasonalRank6-5.png/revision/latest/scale-to-width-down/160?cb=20190130002955"
    elif firstLT == 7:
      ingameRank = "Divine "
      if secondLT == 1:
        ingameRank = ingameRank + "1"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/b7/SeasonalRank7-1.png/revision/latest/scale-to-width-down/160?cb=20190130003022"
      elif secondLT == 2:
        ingameRank = ingameRank + "2"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8f/SeasonalRank7-2.png/revision/latest/scale-to-width-down/160?cb=20190130003026"
      elif secondLT == 3:
        ingameRank = ingameRank + "3"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/fd/SeasonalRank7-3.png/revision/latest/scale-to-width-down/160?cb=20190130003029"
      elif secondLT == 4:
        ingameRank = ingameRank + "4"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/13/SeasonalRank7-4.png/revision/latest/scale-to-width-down/160?cb=20190130003033"
      elif secondLT == 5:
        ingameRank = ingameRank + "5"
        rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/33/SeasonalRank7-5.png/revision/latest/scale-to-width-down/160?cb=20190130003041"
    elif firstLT == 8:
      ingameRank = "Immortal"
      rankimgurl = "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f2/SeasonalRankTop0.png/revision/latest/scale-to-width-down/160?cb=20180606220529"

  response = req.get(rankimgurl)
  img_data2 = response.content
  img2 = ImageTk.PhotoImage(Image.open(BytesIO(img_data2)))
  photo2 = ttk.Label(entry_frame, image=img2)
  photo2.grid(row=1,column=0,padx=5,pady=5,sticky=tk.W)
  rank = ttk.Label(entry_frame,text=f"Rank :\n{ingameRank}")
  rank.grid(row=1,column=1,padx=5,pady=5)
  winratedata = ttk.Label(entry_frame, text=f"Winrate : {winratetotal}")
  winratedata.grid(row=3,column=1,padx=5,pady=5)
  talk("With the choice of data of 1 Nickname 2 Dota Rank 3 Winrate or 4 All of them , please say the number")
  dataasked = speechrecog()
  if "1" in dataasked or "one" in dataasked:
    textdata = f"Your Steam nickname is {nicknamedata}"
    talk(textdata)
  elif "2" in dataasked or "two" in dataasked:
    textdata = f"Your Dota 2 rank is {ingameRank}"
    talk(textdata)
  elif "3" in dataasked or "three" in dataasked:
    textdata = f"Your Dota 2 Lifetime Win Rate is {winrate} with {win} Win out of {total} Games"
    print(textdata)
    talk(textdata)
  elif "4" in dataasked or "four" in dataasked:
    textdata = f"Your Steam nickname is {nicknamedata} your dota 2 rank is {ingameRank} and your winrate is {winrate}"
    talk(textdata)
  else:
    talk("Speech Program has Ended")
  
  root.mainloop()
  

try:
  
  root = tk.Tk()
  root.title("Tracker")
  iconpng = tk.PhotoImage(file = "dotaicon.png")
  root.iconphoto(False, iconpng)
  root.geometry("800x650")
  
  # set minimum window size value
  root.minsize(800, 650)
  root.configure(bg='gray')
  # set maximum window size value
  root.maxsize(800, 650)
  label = tk.Label(root,text="DOTA 2 ACCOUNT TRACKER",font=('Trajan Pro Bold', 26,'bold'),bg='gray')
  label.grid(row=0,column=0)
  entry_frame0 = ttk.Labelframe(root,width=800,height=150)
  # entry_frame0.pack(side=tk.TOP,pady=50,padx=50)
  entry_frame0.grid(row=1,column=0)
  entry_frame0.rowconfigure(9)
  entry_frame0.columnconfigure(9)
  entry_frame0.grid_propagate(0)
  entry_frame0.pack_propagate(0)
  # canvas1 = tk.Canvas(root, width=400, height=300)
  # canvas1.pack(side=tk.LEFT)
  entry1 = tk.Entry(entry_frame0) 
  entry1.grid(row=0,column=1,padx=5,pady=5)
  # canvas1.create_window(200, 80, window=entry1)
  button1 = tk.Button(entry_frame0,text='Check ID!', command=accessID)
  button1.grid(row=1,column=1,padx=5,pady=5)
  # canvas1.create_window(200, 120, window=button1)
  label1 = tk.Label(entry_frame0,text='',width=50)
  label1.grid(row=0,column=3,padx=5,pady=5)
  label2 = tk.Label(entry_frame0,text='Status:')
  label2.grid(row=0,column=2,padx=5,pady=5)
  # canvas1.create_window(200, 200, window=label1)
  button2 = tk.Button(entry_frame0,text='Speech', command=accessIDviaSpeech)
  button2.grid(row=2,column=1,padx=5,pady=5)
  # canvas1.create_window(200, 160, window=button2)
  entry_frame = ttk.Labelframe(root,width=800,height=500)
  # entry_frame.pack(pady=75,padx=50)
  entry_frame.grid(row=2,column=0)
  entry_frame.rowconfigure(9)
  entry_frame.columnconfigure(9)
  entry_frame.grid_propagate(0)
  entry_frame.pack_propagate(0)

  # frame1 = tk.Frame(root, highlightbackground="blue", highlightthickness=2)
  # frame1.pack(padx=20, pady=20)
  # Entry1
  root.mainloop()
except:
  pass


