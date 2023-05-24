import tkinter as tk
from tkinter import ttk
import requests as req
from PIL import ImageTk, Image
import os
from io import BytesIO
import steamid
import steamid_converter.Converter as Converter

api_key = "bca71228-5abf-4825-8ff5-ea2ce7afb60e"
def accessID():
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
  
  img_url = json_data['profile']['avatarfull']
  response = req.get(img_url)
  img_data1 = response.content
  img1 = ImageTk.PhotoImage(Image.open(BytesIO(img_data1)))

  entry_frame = ttk.Labelframe()
  entry_frame.pack(side=tk.RIGHT,pady=50,padx=50)
    # Username Entry
  photo1 = ttk.Label(entry_frame, image=img1)
  photo1.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)
  nicknamedata = json_data['profile']['personaname']
  nickname = ttk.Label(entry_frame,text=f"Nick :\n  {nicknamedata}")
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
  rank = ttk.Label(entry_frame,text=f"Rank :\n  {ingameRank}")
  rank.grid(row=1,column=1,padx=5,pady=5)
  root.mainloop()


root = tk.Tk()


canvas1 = tk.Canvas(root, width=400, height=300)
canvas1.pack(side=tk.LEFT)
entry1 = tk.Entry(root) 
canvas1.create_window(200, 140, window=entry1)
button1 = tk.Button(text='Check ID!', command=accessID)
canvas1.create_window(200, 180, window=button1)
root.mainloop()



