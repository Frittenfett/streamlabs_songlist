# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import json
import codecs
import os
import clr
import random
import time

clr.AddReference("IronPython.Modules.dll")
import urllib

# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Songlist"
Website = "https://www.twitch.tv/frittenfettsenpai"
Description = "A songlist for your stream."
Creator = "frittenfettsenpai"
Version = "1.0.1"


# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global settings
    settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")

    try:
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8")
    except:
        settings = {
            "command": "!songlist",
            "defaultAmount": "10",
            "maxAmount": "15",
        }
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings
    if data.IsChatMessage():
        user = data.User
        username = Parent.GetDisplayName(user)

        if (data.GetParam(0).lower() == settings["command"]):

            if data.GetParamCount() > 1:
                limit = int(data.GetParam(1))
            else:
                limit = int(settings["defaultAmount"])

            if limit < 0 or limit > int(settings["maxAmount"]):
                Parent.SendTwitchMessage("{0} Limit has to be between 1 and {1}!".format(username, settings["defaultAmount"]))
                return

            songs = Parent.GetSongQueue(limit)
            if len(songs) == 0:
                Parent.SendTwitchMessage("Nothing is in the songlist yet.")
                return
            songList = ""
            count = 1
            for obj in songs:
                if count > 1:
                    songList = songList + " | "
                songList = songList + str(count)+": " + obj.Title
                count = count + 1

            Parent.SendTwitchMessage(songList)
    return


# ---------------------------------------
#    [Required] Tick Function
# ---------------------------------------
def Tick():
    return