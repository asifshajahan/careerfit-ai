@echo off
echo ============================================
echo   CareerFit AI - Starting Backend Server
echo ============================================
echo.
cd /d "%~dp0backend"
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting FastAPI server...
echo Backend will be available at: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Open frontend/index.html in your browser to use the app.
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
