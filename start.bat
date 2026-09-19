@echo off
echo ========================================================
echo   Starting Kirana Mitra AI (Voice + Camera Inventory)
echo ========================================================
echo.

REM Start Backend
start "Kirana Backend (FastAPI)" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

REM Start Frontend
start "Kirana Frontend (React Vite)" cmd /k "cd frontend && npm run dev"

echo Backend running on: http://127.0.0.1:8000
echo Frontend running on: http://localhost:5173
echo.
pause
