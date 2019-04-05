@echo off
REM the file for starting the test server
REM set the app variable, can be changed to any entry point
set FLASK_ENV=development
set FLASK_APP=main.py
REM start the app
flask run