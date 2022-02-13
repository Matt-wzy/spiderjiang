@echo off&(cd/d "%~dp0")&(cacls "%SystemDrive%\System Volume Information" >nul 2>&1)||(color 4f&echo 请右键“以管理员身份运行”&echo.&pause&exit /b)
powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe -OutFile python-install.exe"
python-install.exe /passive InstallAllUsers=1 PrependPath=1
pip install -r requirements.txt 
