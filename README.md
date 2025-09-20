# lpawards.py
Python-based award calculation from LeaguePals data

Goal is to compile with pyinstaller so users don't need Python

# Using:
* launch program
* click Login
* enter LeaguePals userid (email) and password
* do one of:
  * click Send - login without saving
  * click Save & Send - credentials will be cached locally and prepopulated next time
* (your leagues should populate)
* select a league from the dropdown
* click Get Info to query scores for league
  * note this will take some time during which the UI won't respond to input
* click Calculate
* (eligible awards will be displayed)

# TODO
* Implement github actions to compile binary for Windows
* Add Mac build
* Allow listing, adding, editing award definitions
* Move all output from launching terminal to on-screen Text window

