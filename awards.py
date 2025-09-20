#!/usr/bin/python3
import json
import sys

# award definition format
#{ 
#  award_type: "relative|absolute|triplicate",
#  unit: "game|series",  
#  score_value: 50, # min threshold score (absolute) or diff from average (relative) 
#  avg_ceiling: 140 # default 300 or no ceiling
#  min_games: 12    # minimum previous games to be eligible
#}
  
def console_print(input):
  print(input)

def check_bowler_award(award=None, bowler_info=None, output=console_print):
  score_value = award.get("score_value", 0)
  avg_ceiling = award.get("avg_ceiling", 301)
  min_games = award.get("min_games", 0)
  unit = award.get("unit", "game")
  award_type = award.get("type", "absolute")

  bname = bowler_info["user"]["name"]
  team = bowler_info["team"]["name"]
  games = 0
  if unit == "series":
    for stat in bowler_info["stats"]:
      # series award only if all games are regular
      if stat["status1"] == "R" and stat["status2"] == "R" and stat["status3"] == "R":
        if games >= min_games and award_type == "absolute" and stat["average"] < avg_ceiling and stat["scratchPins"] >= score_value:
          output(json.dumps({"series": score_value, "bowler": bowler_info["user"]["name"], "week": stat["week"], "series": stat["scratchPins"]}))
        if games >= min_games and award_type == "relative" and stat["average"] < avg_ceiling and stat["scratchPins"] - stat["average"] * 3 >= score_value:
          output(json.dumps({"series over": score_value, "bowler": bowler_info["user"]["name"], "week": stat["week"], "average": stat["average"], "series": stat["scratchPins"]}))
        if games >= min_games and award_type == "triplicate" and stat["average"] < avg_ceiling and stat["game1"] == stat["game2"] and stat["game2"] == stat["game3"]:
          output(json.dumps({"triplicate": stat["game1"], "bowler": bowler_info["user"]["name"], "week": stat["week"]}))
      # each individual game counts toward games bowled - TODO - prebowls should count here too
      if stat["status1"] == "R":
        games += 1
      if stat["status2"] == "R":
        games += 1
      if stat["status3"] == "R":
        games += 1
  if unit == "game":
    #print("-> game", end="")
    for stat in bowler_info["stats"]:
      for game in [[stat["game1"],stat["status1"]],[stat["game2"],stat["status2"]],[stat["game3"],stat["status1"]]]:
        if game[1] != "R":
          continue
        if games >= min_games and award_type == "absolute" and stat["average"] < avg_ceiling and game[0] >= score_value:
          output(json.dumps({"award": award["name"], "bowler": bowler_info["user"]["name"], "week": stat["week"], "average": stat["average"], "game": game[0]}))
        if games >= min_games and award_type == "relative" and stat["average"] < avg_ceiling and game[0] - stat["average"] >= score_value:
          output(json.dumps({"award": award["name"], "bowler": bowler_info["user"]["name"], "week": stat["week"], "average": stat["average"], "game": game[0]}))
        games += 1

def check_bowler_awards(binfo=None, output=console_print):
  check_bowler_award(award = {
    "name": "50 over game < 140",
    "type": "relative",
    "avg_ceiling": 140,
    "min_games": 12,
    "unit": "game",
    "score_value": 50 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "name": "75 over game",
    "type": "relative",
    "min_games": 12,
    "unit": "game",
    "score_value": 75 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "name": "100 over game",
    "type": "relative",
    "min_games": 12,
    "unit": "game",
    "score_value": 100 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "name": "triplicate (igbo)",
    "type": "triplicate",
    "unit": "series",
    "min_games": 0,
  }, bowler_info=binfo, output=output)

def check_bowler_awards_old(binfo=None):
  game50 = []
  game75 = []
  game100 = []
  series150 = []
  series200 = []
  series500 = []
  series600 = []
  series700 = []
  triplicate = []
  weeks = {}
  bstats = {}
  team = {}
  games = {}

  bname = binfo["user"]["name"]
  team[bname] = binfo["team"]["name"]
  bstats[bname] = {}
  for stat in binfo["stats"]:
    weeks[stat["week"]] = 1
    bstats[bname][stat["week"]] = {
      "average" : stat["average"],
      "game1"   : stat["game1"],
      "game2"   : stat["game2"],
      "game3"   : stat["game3"],
      "handicap": stat["handicap"],
    }
    # 12 games bowled: 75/100 over game, 150/200 over series
    if bname not in games:
      games[bname] = 0
    if games[bname] >= 12:
      if (stat["game1"] == stat["game2"] == stat["game3"] and stat["status1"] == stat["status2"] == stat["status3"] == "R"):
        print(json.dumps({ "award": "triplicate", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "average": stat["average"], "game": game }))
      for gamestatus in ((stat["game1"], stat["status1"]), (stat["game2"],stat["status2"]), (stat["game3"],stat["status3"])):
        game = gamestatus[0];
        if (gamestatus[1] != "R"):
          #print("skip absent bowler %s, week %d\n" % (bname, stat["week"]))
          next;
        if game >= stat["average"] + 75:
          print(json.dumps({"award": "75 over game", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "average": stat["average"], "game": game }))
        if game >= stat["average"] + 100:
          print(json.dumps( { "award": "100 over game", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "average": stat["average"], "game": game }))
        if stat["average"] <140 and game >= stat["average"] + 50:
          print(json.dumps( { "award": "50 over game < 140", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "average": stat["average"], "game": game }))
      series = stat["game1"] + stat["game2"] + stat["game3"]
      if series >= stat["average"] * 3 + 150:
        print(json.dumps( { "award": "150 over series", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "s-average": stat["average"] * 3, "series": series }))
      if series >= stat["average"] * 3 + 200:
        print(json.dumps( { "award": "200 over series", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "s-average": stat["average"] * 3, "series": series }))
      if stat["average"] <140 and series >= 500:
        print(json.dumps( { "award": "500 series < 140", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "s-average": stat["average"] * 3, "series": series }))
      if stat["average"] <175 and series >= 600:
        print(json.dumps( { "award": "600 series < 175", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "s-average": stat["average"] * 3, "series": series }))
      if series >= 700:
        print(json.dumps( { "award": "700 series", "bowler": bname, "week": stat["week"], "date": stat["date"], "games": games[bname], "s-average": stat["average"] * 3, "series": series }))
    games[bname] += 3

def get_bowler_stats():
  weekkeys = list(weeks.keys())
  weekkeys.sort()
  print(f"bowler	team	", end="")
  for week in weekkeys:
    print(f"{week}-avg	{week}-hcp	{week}-1	{week}-2	{week}-3	{week}-avg2	", end="")
  print("pins	games	average")

  for bowler in bstats.keys():
    print(f"{bowler}	{team[bowler]}	", end="")
    pins=0
    games=0
    for week in weekkeys:
      if week in bstats[bowler]:
        wstat = bstats[bowler][week]
        games+=3
        pins += wstat['game1'] + wstat['game2'] + wstat['game3']
        print(f"{wstat['average']}	{wstat['handicap']}	{wstat['game1']}	{wstat['game2']}	{wstat['game3']}	{int(pins/games)}	", end="")
        
      else:
        print("						", end="")
    print(f"{pins}	{games}	{int(pins/games)}")