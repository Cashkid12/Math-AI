@echo off
echo ========================================
echo   EQUAI AI - COMPLETE STARTUP
echo ========================================
echo.
echo Starting Backend Server (Flask)...
start cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak > nul
echo.
echo Starting Frontend Server (Vite)...
start cmd /k "cd frontend && npm run dev"
echo.
echo ========================================
echo   Both servers are starting...
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
pause
