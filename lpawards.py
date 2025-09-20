#!/usr/bin/python3

import http
import requests
import sys
import json
import os
import tkinter as tk
from tkinter import ttk
import leaguepals as lp
import awards
import cachefiles

def login_do_savesend():
  print('-- save credentials')
  cachefiles.save_auth_info(username=username.get(), password=password.get())
  login_do_send()

def login_do_send():
  print('-- login')
  if lp.login(username=username.get(), password=password.get()):
    text.insert(index='end', chars = "logged in\n")
    print(json.dumps(lp.get_my_info(), indent=2))
    update_league_selections()
  else:
    text.insert(index='end', chars = "login failed\n")
  auth_win.destroy()

def update_league_selections():
  global my_leagues
  my_leagues = lp.get_my_leagues()
  if my_leagues:
    league_cb.set("Select League")
    print("-- my queried leagues --")
  else:
    my_leagues = cachefiles.get_cached_leagues()
    if not my_leagues:
      return None
    print(json.dumps(my_leagues))
    league_cb.set("Select Cached League")
    print("-- my cached leagues --")
  print(json.dumps(my_leagues, indent=2))
  league_selections = []
  for league in my_leagues:
    league_selections.append(league["league_name"])
  league_cb['values'] = league_selections
  league_cb.pack()

def do_league_selection(event):
  global league_info
  league_index = league_cb.current()
  print(json.dumps(my_leagues[league_index]))
  league_info = cachefiles.get_league_info(my_leagues[league_index]["league_id"])
  if league_info:
    text.insert(index='end', chars = "loaded " + my_leagues[league_index]["league_name"] + " from cached file\n")
    text.insert(index='end', chars = "press 'Get Info' to refresh data from LeaguePals\n")
    text.insert(index='end', chars = "press 'Calculate' to check for awards\n")
    calculate_button.config(state=tk.NORMAL)
  else:
    text.insert(index='end', chars = "no cached data for " + my_leagues[league_index]["league_name"] + "\n")
    text.insert(index='end', chars = "press 'Get Info' to retrieve data from LeaguePals\n")
  info_button.config(state=tk.NORMAL)
  
def do_login():
  auth = cachefiles.get_auth_info()
  username.set(auth["username"])
  password.set(auth["password"])
  global auth_win
  auth_win = tk.Toplevel(root)
  auth_win.title("LeaguePals Login Info")
  user_label = tk.Label(auth_win, text='login email:')
  user_label.pack(pady=5)
  username_entry = tk.Entry(auth_win, textvariable=username)
  username_entry.pack(padx=8)
  password_label = tk.Label(auth_win, text='password:')
  password_label.pack(pady=5)
  password_entry = tk.Entry(auth_win, show='*', textvariable=password)
  password_entry.pack(padx=8)
  login_buttons = tk.Frame(auth_win)
  login_buttons.pack(expand=False)
  button = tk.Button(login_buttons, text="Send", command=login_do_send)
  button.pack(pady=5, side=tk.LEFT)
  button = tk.Button(login_buttons, text="Save & Send", command=login_do_savesend)
  button.pack(pady=5, side=tk.LEFT)

def do_get_info():
  global league_info
  league_info = lp.get_league_info(
    league_id=my_leagues[league_cb.current()]["league_id"], 
    center_id=my_leagues[league_cb.current()]["center_id"])
  if not league_info:
    text.insert(index='end', chars = "failed to retrieve data for " + my_leagues[league_cb.current()]["league_name"] + "\n")
    return None
  cachefiles.save_league_info(league_info)
  calculate_button.config(state=tk.NORMAL)

def do_calculate():
  global league_info
  for bowler_info in league_info["bowlers"]:
    awards.check_bowler_awards(bowler_info)
  print("-----")
  for bowler_info in league_info["bowlers"]:
    awards.check_bowler_awards_old(bowler_info)

def textEvent(event):
  if 12 == event.state and event.keysym == "c":
    return
  else:
    return "break"

lp_session = None
auth_win = None
root = tk.Tk()
root.title("LeaguePals Awards")
username = tk.StringVar()
password = tk.StringVar()
my_leagues = []
league_info = {}

button_area = tk.Frame(root)
button_area.pack(expand=False)

login_button = tk.Button(button_area, text="Login", command=do_login)
login_button.pack(side=tk.LEFT, expand=True)

league_selections = []
league_cb = ttk.Combobox(button_area, values=league_selections, width=40)
league_cb.set("Login to populate league choices")
league_cb.pack(side=tk.LEFT)
league_cb.bind('<<ComboboxSelected>>', do_league_selection)
update_league_selections()

info_button = tk.Button(button_area, text="Get Info", command=do_get_info)
info_button.config(state=tk.DISABLED)
info_button.pack(side=tk.LEFT)

calculate_button = tk.Button(button_area, text="Calculate", command=do_calculate)
calculate_button.config(state=tk.DISABLED)
calculate_button.pack(side=tk.LEFT)

exit_button = tk.Button(button_area, text="Exit", command=root.destroy)
exit_button.pack(side=tk.RIGHT)
text = tk.Text(root, height=8)
text.bind("<Key>", lambda e: textEvent(e))
text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

root.mainloop()
sys.exit()