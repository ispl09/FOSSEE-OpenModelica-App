@echo off
SET PATH=;D:/Users/DELL/OneDrive/Desktop/bin/;%PATH%;
SET ERRORLEVEL=
CALL "%CD%/TwoConnectedTanks.exe" %*
SET RESULT=%ERRORLEVEL%

EXIT /b %RESULT%
