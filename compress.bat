SET SRCDIR=septima_flow
SET PLUGINNAME=septima_flow

SET TMPDIR=TMP
SET DESTDIR=%TMPDIR%\%PLUGINNAME%
SET ARCHIVENAME=%PLUGINNAME%.zip
SET COPYFILES=%SRCDIR%\*.py,%SRCDIR%\metadata.txt
SET COPYDIRS=

MKDIR %DESTDIR%

FOR %%f IN (%COPYFILES%) DO (
	COPY %%f %DESTDIR%
	IF ERRORLEVEL 1 PAUSE
)

SET COMPRESSEXE="C:\Program Files\7-Zip\7z.exe"
SET COMPRESSCOMMAND=a -r %ARCHIVENAME% %PLUGINNAME%

CD %TMPDIR%
%COMPRESSEXE% %COMPRESSCOMMAND%
IF ERRORLEVEL 1 PAUSE
CD ..

RMDIR /S /Q %DESTDIR%