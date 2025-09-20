#!/usr/bin/python3

import os.path
import glob
import json
import re

# constant for now, maybe changeable later
cachepath = "cache/"

def init():
    if not os.path.isdir(cachepath):
       os.makedirs(cachepath) 

def get_auth_info():
    if os.path.isfile(cachepath + 'auth.json'):
        with open(cachepath + 'auth.json') as auth_json:
            auth = json.load(auth_json)
            auth_json.close()
            return auth
    return {
        "username": "abc",
        "password": "def"
    }

def save_auth_info(username, password):
    auth = {
        "username": username,
        "password": password
    }
    auth_str = json.dumps(auth, indent=4)
    with open(cachepath + "auth.json", "w") as auth_json:
        auth_json.write(auth_str)


def get_league_info(league_id=None):
    if not league_id:
        return None
    if os.path.isfile(cachepath + league_id + ".json"):
        with open(cachepath + league_id + ".json") as league_json:
            league_info = json.load(league_json)
            league_json.close()
            #print("get_league_info returns " + json.dumps(league_info))
            return league_info
    return None

def save_league_info(league_info):
    league_id = league_info["_id"]
    league_str = json.dumps(league_info, indent=4)
    with open(cachepath + league_id + ".json", "w") as league_json:
        league_json.write(league_str)

# returns an array of any cached leagues in this format:
#  {
#    "center_id": "62d978814cfb9220133832a0",
#    "center_name": "Bowlero Raleigh",
#    "league_id": "62e6923b55b9a0101c2d8b61",
#    "league_name": "Kings & Queens 22",
#    "date_start": "2022-09-01T00:00:00.000Z"
#  }
def get_cached_leagues():
    leagues = []
    for filename_raw in glob.glob(cachepath + "*.json"):
        filename = filename_raw.replace("\\","/")
        print(filename)
        if re.match(r"^cache/[0-9a-f]{24}\.json", filename):
            print(f"{filename}\n")
            with open(filename) as league_json:
                league_info = json.load(league_json)
                league_json.close
                leagues.append({
                    "center_id": league_info["center"],
                    "center_name": league_info["bowlers"][0]["stats"][0]["center"],
                    "league_id": league_info["_id"],
                    "league_name": league_info["name"],
                    "date_start": league_info["seasons"][0]["dateStart"],
                })
    return leagues