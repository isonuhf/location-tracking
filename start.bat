@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════╗
echo ║   智能硬件位置追踪系统 - 启动脚本              ║
echo ╚════════════════════════════════════════════════╝
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python未安装
    pause
    exit /b 1
)

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Node.js未安装
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i

echo [OK] Python已安装: %PYTHON_VER%
echo [OK] Node.js已安装: %NODE_VER%
echo.

REM 启动后端
echo [启动] 后端服务...
cd backend
start "Backend Server" python main.py
echo [OK] 后端进程已启动
timeout /t 3 /nobreak

REM 启动前端
echo [启动] 前端服务...
cd ..\frontend
start "Frontend Server" npm run dev
echo [OK] 前端进程已启动

echo.
echo ╔════════════════════════════════════════════════╗
echo ║              服务已启动                        ║
echo ╚════════════════════════════════════════════════╝
echo.
echo 后端服务: http://localhost:8000
echo 前端服务: http://localhost:5173
echo.
echo 请在浏览器中打开: http://localhost:5173
echo.
pause
