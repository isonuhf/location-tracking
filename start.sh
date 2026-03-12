#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║   智能硬件位置追踪系统 - 启动脚本              ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# 检查Python
if ! command -v python &> /dev/null; then
    echo "[FAIL] Python未安装"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "[FAIL] Node.js未安装"
    exit 1
fi

echo "[OK] Python已安装: $(python --version)"
echo "[OK] Node.js已安装: $(node --version)"
echo ""

# 启动后端
echo "[启动] 后端服务..."
cd backend
python main.py &
BACKEND_PID=$!
echo "[OK] 后端进程ID: $BACKEND_PID"

# 等待后端启动
sleep 3

# 启动前端
echo "[启动] 前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "[OK] 前端进程ID: $FRONTEND_PID"

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║              服务已启动                        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "后端服务: http://localhost:8000"
echo "前端服务: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止所有服务..."
echo ""

# 等待中断
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '[OK] 所有服务已停止'; exit 0" INT

wait
