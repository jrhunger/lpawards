#!/usr/bin/python3
import requests
import sys

session = None

def checkresponse(r):
  if r.status_code != 200:
    print("==> status = " + str(r.status_code))
    print(r.headers)
    sys.exit(1)

def login(username="", password=""):
    if not username or not password:
        return False
    global session
    session = requests.Session()
    login = {'email': username,
           'password': password,
           'redirectTo': '' 
           }
    r = session.post('https://www.leaguepals.com/login', json=login)
    checkresponse(r)
    print(r.text)
    return True

def get_my_info():
    print('-- myInfo')
    r = session.get('https://www.leaguepals.com/myInfo')
    checkresponse(r)
    return r.json()

# returns an array of leagues in this format:
#  {
#    "center_id": "62d978814cfb9220133832a0",
#    "center_name": "Bowlero Raleigh",
#    "league_id": "62e6923b55b9a0101c2d8b61",
#    "league_name": "Kings & Queens 22",
#    "date_start": "2022-09-01T00:00:00.000Z"
#  }
def get_my_leagues():
    if not session:
        return None
    r = session.get('https://www.leaguepals.com/myTeams')
    checkresponse(r)
    #print(r.text)
    leagues = []
    for team in r.json()["data"]:
        leagues.append({
            "center_id": team["center"]["_id"],
            "center_name": team["center"]["centerName"],
            "league_id": team["league"]["_id"],
            "league_name": team["league"]["name"],
            "date_start": team["league"]["seasons"][0]["dateStart"],
        })
    return leagues

# returns league info which is the upstream LeaguePals league json object,
# augmented with a new key "bowlers", the value of which is an array of all
# bowlers in the league. The bowler objects are the upstream LeaguePals json
# augmented with a "team" key, the value of which is the team id
def get_league_info(league_id = None, center_id = None):
    global session
    if not session:
        print("attempt to get league info without session")
        return False
    r = session.get('https://www.leaguepals.com/fullLeagueInfoBowler?id=' + league_id)
    checkresponse(r)
    league_info = r.json()["data"]
    team_limit = 50
    team_count = 0
    league_info["bowlers"] = []
    for team in league_info["teams"]:
        print(team["_id"] + "	" + team["name"])
        r = session.get('https://www.leaguepals.com/loadIndividualTeam?id=' + team["_id"] + '&noPre=false')
        checkresponse(r)
        #print(r.text)
        teaminfo = r.json()
        for bowler in teaminfo["data"]:
            print("	" + bowler["_id"] + "	" + bowler["name"])
            r2 = session.get('https://www.leaguepals.com/my-leagues-stats' + 
                    '?center=' + center_id +
                    '&league=' + league_id +
                    '&userid=' + bowler["_id"])
            checkresponse(r2)
            #print(r2.text)
            bowlerinfo = r2.json()
            bowlerinfo["data"]["team"] = { "id": team["_id"], "name": team["name"]}
            league_info["bowlers"].append(bowlerinfo["data"])
        team_count += 1
        if team_count >= team_limit:
            return league_info
    return league_info