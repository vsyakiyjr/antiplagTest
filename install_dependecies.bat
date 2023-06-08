@echo off
set ABS_PATH=%~dp0

"%ABS_PATH%\installations\python-3.9.13-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1
"%ABS_PATH%\installations\jdk-8u361-windows-x64.exe" /s ADDLOCAL="ToolsFeature,SourceFeature,PublicjreFeature"
cd "%ABS_PATH%"
python -m venv venv
cmd.exe /K "cd "%ABS_PATH%" && venv\Scripts\activate.bat && pip install -r requirements.txt"