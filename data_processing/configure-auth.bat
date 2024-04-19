@echo off
setlocal

cd /d "%~dp0"

:: Define the directory containing the JSON files
set "DIRECTORY=authentication"

:: Enable delayed expansion to handle the loop and variable setting correctly
setlocal enabledelayedexpansion

:: Initialize variable to store the path of the first JSON file
set "FIRST_JSON="

:: Iterate over JSON files in the directory and pick the first one

for %%F in ("%DIRECTORY%\*.json") do (
    if not defined FIRST_JSON (
        echo FOUND %%F
        set "FIRST_JSON=%%F"
    )
)

:: Check if a JSON file was found and set the environment variable
if defined FIRST_JSON (
    set "GOOGLE_APPLICATION_CREDENTIALS=%FIRST_JSON%"
    echo Environment variable GOOGLE_APPLICATION_CREDENTIALS set to %GOOGLE_APPLICATION_CREDENTIALS%
    setx GOOGLE_APPLICATION_CREDENTIALS "%FIRST_JSON%"

) else (
    echo No JSON files found in the directory.
)

:: Keep the window open to view the output (remove this line in scheduled tasks or automated runs)
pause

endlocal
