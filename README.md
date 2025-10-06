# lpawards.py
Python-based award calculation from LeaguePals data
Uses tkinter

# Initial Run: Accept Security Warnings
These binaries are not signed and therefore Windows and iOS make it difficult to run.
The following will need to be done each time a new version is downloaded.
## Windows
* Open a command prompt and cd to the directory where you unpacked lpawards.exe
* Type .\lpawards
* The rest of this may or may not be needed
* A blue dialog will pop up saying "Windows protected your PC"
* Click "More info"
* Click the "Run Anyway" button that appears

## Mac iOS
* Try to open the file once (an error will be displayed with no option to run it)
* Open Settings -> Privacy & Security
* Under the Security section there should be a box saying: `"lpawards" was blocked to protect your Mac`
* Click "Open Anyway"
* Click "Open Anyway" again on the popup that asks if you want to move it to the trash

# Using:
* launch program (see security notes below)
* click Login
* enter LeaguePals userid (email) and password
* do one of:
  * click Send - login without saving
  * click Save & Send - credentials will be cached locally and pre-populated next time
* (your leagues should populate)
* select a league from the dropdown
* click Get Info to query scores for league
  * note this will take some time during which the UI won't respond to input
  * at the end, the retrieved scores will be cached to disk in the local cache folder
* click Calculate
* (eligible awards will be displayed)

# TODO
* Sign binaries so they can run without security warnings
* Allow listing, adding, editing award definitions
* Remove launching terminal output