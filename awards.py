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
          output(json.dumps({"org": award["org"], "award": award["name"], "series": score_value, "bowler": bowler_info["user"]["name"], "week": stat["week"], "series": stat["scratchPins"]}))
        if games >= min_games and award_type == "relative" and stat["average"] < avg_ceiling and stat["scratchPins"] - stat["average"] * 3 >= score_value:
          output(json.dumps({"org": award["org"], "award": award["name"], "series over": score_value, "bowler": bowler_info["user"]["name"], "week": stat["week"], "average": stat["average"], "series": stat["scratchPins"]}))
        if games >= min_games and award_type == "triplicate" and stat["average"] < avg_ceiling and stat["game1"] == stat["game2"] and stat["game2"] == stat["game3"]:
          output(json.dumps({"org": award["org"], "award": award["name"], "triplicate": stat["game1"], "bowler": bowler_info["user"]["name"], "week": stat["week"]}))
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
          output(json.dumps({"org": award["org"], "award": award["name"], "bowler": bowler_info["user"]["name"], "week": stat["week"], "average": stat["average"], "game": game[0]}))
        if games >= min_games and award_type == "relative" and stat["average"] < avg_ceiling and game[0] - stat["average"] >= score_value:
          output(json.dumps({"org": award["org"], "award": award["name"], "bowler": bowler_info["user"]["name"], "week": stat["week"], "average": stat["average"], "game": game[0]}))
        games += 1

def check_bowler_awards(binfo=None, org="USBC", output=console_print):
  if org == "USBC":
    check_igbo_awards(binfo, output)
  if org == "IGBO":
    check_usbc_awards(binfo, output)

def check_usbc_awards(binfo=None, output=console_print):
  check_bowler_award(award = {
    "org": "USBC",
    "name": "75 over game",
    "type": "relative",
    "min_games": 0,
    "unit": "game",
    "score_value": 75 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "USBC",
    "name": "100 over game",
    "type": "relative",
    "min_games": 12,
    "unit": "game",
    "score_value": 100 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "USBC",
    "name": "150 over series",
    "type": "relative",
    "min_games": 12,
    "unit": "series",
    "score_value": 150 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "USBC",
    "name": "200 over series",
    "type": "relative",
    "min_games": 12,
    "unit": "series",
    "score_value": 200 
  }, bowler_info=binfo, output=output)

def check_igbo_awards(binfo=None, output=console_print):
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "triplicate",
    "type": "triplicate",
    "unit": "series",
    "min_games": 0,
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "50 over game < 140",
    "type": "relative",
    "avg_ceiling": 140,
    "unit": "game",
    "score_value": 50 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "75 over game",
    "type": "relative",
    "unit": "game",
    "score_value": 75 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "100 over game",
    "type": "relative",
    "unit": "game",
    "score_value": 100 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "500 series < 140",
    "type": "absolute",
    "avg_ceiling": 140,
    "unit": "series",
    "score_value": 500 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "600 series < 175",
    "type": "absolute",
    "avg_ceiling": 175,
    "unit": "series",
    "score_value": 600 
  }, bowler_info=binfo, output=output)
  check_bowler_award(award = {
    "org": "IGBO",
    "name": "700 series",
    "type": "absolute",
    "unit": "series",
    "score_value": 700 
  }, bowler_info=binfo, output=output)

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