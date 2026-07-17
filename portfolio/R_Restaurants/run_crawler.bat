@echo off
rem ------------------------------------------------------------
rem Recruitment Crawler - Setup & Execution Script
rem ------------------------------------------------------------

rem 1️⃣ Create virtual environment (if not exists)
if not exist venv (
    echo Creating virtual environment... 
    python -m venv venv
)

rem 2️⃣ Activate virtual environment
call venv\Scripts\activate

rem 3️⃣ Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

rem 4️⃣ Install Playwright browsers (Chromium)
python -m playwright install chromium

rem 5️⃣ Run the crawler
python crawler\main.py

pause
