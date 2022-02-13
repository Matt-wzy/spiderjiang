@echo off&(cd/d "%~dp0")&(cacls "%SystemDrive%\System Volume Information" >nul 2>&1)||(color 4f&echo ���Ҽ����Թ���Ա�������С�&echo.&pause&exit /b)
pip install -r requirements.txt 
