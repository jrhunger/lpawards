#!/usr/bin/python3

import json
import sys

print("last	first	pins	games	average")
for i, arg in enumerate(sys.argv):
  if i == 0:
    continue
  bfile = open(arg, "r")
  binfo = json.load(bfile)
  bfile.close()
  games = 0
  total = 0
  bname = binfo["data"]["user"]["name"].split(" ")
  for score in binfo["data"]["games"]:
    games += 1
    total += score
  average = int(total / games)
  print(f"{bname[1]}	{bname[0]}	{total}	{games}	{average}")
