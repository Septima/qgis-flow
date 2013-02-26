ECHO Publish to local user QGIS

SET DEST=%USERPROFILE%\.qgis\python\plugins\septima_flow
del %DEST%\*.pyc

IF NOT EXIST %DEST% MD %DEST%

REM EXTENSIONS TO COPY
SET EXT=png,py,qrc,ui

FOR /D %%e IN (%EXT%) DO COPY septima_flow\*.%%e %DEST%