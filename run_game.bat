@echo off
echo ==========================================
echo   Lancement du Projet Timeline CardGame
echo ==========================================

echo.
echo [1/2] Lancement du Backend (FastAPI)...
start "Backend - Timeline" cmd /k "cd backend && .\venv\Scripts\python -m uvicorn main:app --reload"

echo [2/2] Lancement du Frontend (Vue.js)...
start "Frontend - Timeline" cmd /k "cd frontend && npm run dev"

echo.
echo Les deux services sont en cours de lancement dans des fenêtres séparées.
echo.
pause
