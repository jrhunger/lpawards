#!/usr/bin/python3

import http
import requests
import sys
import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import leaguepals as lp
import awards
import cachefiles

def output_textarea(input):
    global text
    text.insert(index='end', chars = input + "\n")
    text.update()
    text.yview(tk.END)

def login_do_savesend():
  print('-- save credentials')
  cachefiles.save_auth_info(username=username.get(), password=password.get(), output=output_textarea)
  login_do_send()

def login_do_send():
  print('-- login')
  if lp.login(username=username.get(), password=password.get()):
    output_textarea("-- logged in as " + username.get() + " --")
    print(json.dumps(lp.get_my_info(), indent=2))
    update_league_selections()
  else:
    output_textarea("xx login failed xx")
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
    output_textarea("-- loaded " + my_leagues[league_index]["league_name"] + " from cached file --")
    output_textarea("   bowlers: " + str(len(league_info["bowlers"])))
    output_textarea("   retrieved: " + league_info["retrieved"])
    output_textarea("   last bowling date: " + league_info["last_bowled"])
    info_action="refresh"
    output_textarea("press 'Calculate' to check for awards")
    calculate_button.config(state=tk.NORMAL)
  else:
    output_textarea("-- no cached data for " + my_leagues[league_index]["league_name"] + " --")
    info_action="retrieve"
  if(lp.logged_in()):
    info_button.config(state=tk.NORMAL)
    output_textarea("press 'Get Info' to " + info_action + " data from LeaguePals")
  else:
    output_textarea("Login and press 'Get Info' to " + info_action + " data from LeaguePals")

def do_settings():
  global set_win
  set_win = tk.Toplevel(root)
  set_win.title("Adjust Settings")
  set_win.columnconfigure(0, weight=2)
  set_win.columnconfigure(1, weight=1)
  set_win.rowconfigure(0, weight=1)
  set_win.rowconfigure(1, weight=1)
  maxteams_label = tk.Label(set_win, text="max teams retrieved (for testing)")
  maxteams_label.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
  maxteams_entry = tk.Entry(set_win, textvariable=maxteams)
  maxteams_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
  maxteams_entry.bind("<Key>", lambda e: only_digits(e))
  update_settings_button = tk.Button(set_win, text="Update", command=settings_do_update)
  update_settings_button.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

def settings_do_update():
  print("update settings")
  set_win.destroy()
  
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
  output_textarea("-- querying LeaguePals for " + my_leagues[league_cb.current()]["league_name"] + " --")
  league_info = lp.get_league_info(
    league_id=my_leagues[league_cb.current()]["league_id"], 
    center_id=my_leagues[league_cb.current()]["center_id"],
    output=output_textarea, maxteams=int(maxteams.get()))
  if not league_info:
    output_textarea("xx failed to retrieve data for " + my_leagues[league_cb.current()]["league_name"] + " xx")
    return None
  cachefiles.save_league_info(league_info, output=output_textarea)
  calculate_button.config(state=tk.NORMAL)

def do_calculate():
  global league_info
  output_textarea("-- calculating awards --")
  for bowler_info in league_info["bowlers"]:
    awards.check_bowler_awards(bowler_info, output=output_textarea)

def no_input(event):
  # only allows copying text from window, no input
  if 12 == event.state and event.keysym == "c":
    return
  else:
    return "break"

def only_digits(event):
  # only allow digits to be typed
  if event.char.isdigit() or event.keysym == "BackSpace":
    return
  return "break"

lp_session = None
auth_win = None
root = tk.Tk()
root.title("LeaguePals Awards")
username = tk.StringVar()
password = tk.StringVar()
maxteams = tk.StringVar()
maxteams.set("999")
my_leagues = []
league_info = {}

button_area = tk.Frame(root)
button_area.pack(expand=False)

login_button = tk.Button(button_area, text="Login", command=do_login)
login_button.pack(side=tk.LEFT, padx=2, expand=True)

league_selections = []
league_cb = ttk.Combobox(button_area, values=league_selections, width=40)
league_cb.set("Login to populate league choices")
league_cb.pack(side=tk.LEFT, padx=2)
league_cb.bind('<<ComboboxSelected>>', do_league_selection)
update_league_selections()

info_button = tk.Button(button_area, text="Get Info", command=do_get_info)
info_button.config(state=tk.DISABLED)
info_button.pack(side=tk.LEFT, padx=2)

calculate_button = tk.Button(button_area, text="Calculate", command=do_calculate)
calculate_button.config(state=tk.DISABLED)
calculate_button.pack(side=tk.LEFT, padx=2)

settings_button = tk.Button(button_area, text="Settings", command=do_settings)
settings_button.pack(side=tk.LEFT, padx=2)

exit_button = tk.Button(button_area, text="Exit", command=root.destroy)
exit_button.pack(side=tk.RIGHT, padx=2)
#text = tk.Text(root, height=8)
text = st.ScrolledText(root, height=25)
text.bind("<Key>", lambda e: no_input(e))
text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

root.mainloop()
sys.exit()