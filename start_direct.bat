@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🚚 运输车队实时追踪系统 - 完整启动（改进版）              ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM 启动后端
echo [1/3] 启动后端服务...
cd backend
start "Backend Server" python main.py
echo       ✓ 后端进程已启动
timeout /t 2 /nobreak

REM 启动前端
echo [2/3] 启动前端服务...
cd ..\frontend
start "Frontend Server" npm run dev
echo       ✓ 前端进程已启动
timeout /t 3 /nobreak

REM 启动模拟硬件
echo [3/3] 启动模拟硬件...
cd ..\backend
start "Vehicle Simulator" python simulate_vehicle_direct.py multi 3
echo       ✓ 模拟硬件进程已启动

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    系统已启动                                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📍 访问地址:
echo    前端应用: http://localhost:5173
echo    后端API: http://localhost:8000
echo    API文档: http://localhost:8000/docs
echo.

echo 🚚 模拟硬件信息:
echo    车辆数量: 3
echo    上报间隔: 15秒
echo    速度: 80 km/h
echo    路线: 北京 → 天津
echo    模式: 直接数据注入（无需MQTT Broker）
echo.

echo 按任意键关闭此窗口...
pause >nul
