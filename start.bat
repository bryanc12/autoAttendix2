@echo off
@setlocal enableextensions
@cd /d "%~dp0"
pip install -r requirements.txt
cls
python main.py
pause