SETLOCAL
CALL C:\osgeo4w\osgeo4w.bat param

SET SRCDIR=septima_flow

ECHO Compiling UI
FOR %%f IN (%SRCDIR%\*.ui) DO CALL pyuic4 -o %%~dpnf.py %%f

ECHO Compiling ressources
FOR %%f IN (%SRCDIR%\*.qrc) DO CALL pyrcc4 -o %%~dpnf.py %%f
ENDLOCAL