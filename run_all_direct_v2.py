#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的启动脚本 - 使用直接数据注入（不需要MQTT Broker）
支持Windows、Linux、macOS
"""
import subprocess
import time
import sys
import os
import platform

def main():
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║                                                                ║")
    print("║     🚚 运输车队实时追踪系统 - 完整启动（改进版）              ║")
    print("║                                                                ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    processes = []
    is_windows = platform.system() == "Windows"

    try:
        # 启动后端
        print("[1/3] 启动后端服务...")
        backend_proc = subprocess.Popen(
            [sys.executable, 'main.py'],
            cwd='backend',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        processes.append(('后端', backend_proc))
        print("      ✓ 后端进程已启动 (PID: {})".format(backend_proc.pid))
        time.sleep(2)

        # 启动前端
        print("[2/3] 启动前端服务...")
        if is_windows:
            # Windows上使用shell=True和npm.cmd
            frontend_proc = subprocess.Popen(
                'npm run dev',
                cwd='frontend',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        else:
            # Linux/Mac上直接使用npm
            frontend_proc = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd='frontend',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
        processes.append(('前端', frontend_proc))
        print("      ✓ 前端进程已启动 (PID: {})".format(frontend_proc.pid))
        time.sleep(3)

        # 启动模拟硬件
        print("[3/3] 启动模拟硬件...")
        simulator_proc = subprocess.Popen(
            [sys.executable, 'simulate_vehicle_direct.py', 'multi', '3'],
            cwd='backend',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        processes.append(('模拟硬件', simulator_proc))
        print("      ✓ 模拟硬件进程已启动 (PID: {})".format(simulator_proc.pid))

        print("\n╔════════════════════════════════════════════════════════════════╗")
        print("║                    系统已启动                                 ║")
        print("╚════════════════════════════════════════════════════════════════╝\n")

        print("📍 访问地址:")
        print("   前端应用: http://localhost:5173")
        print("   后端API: http://localhost:8000")
        print("   API文档: http://localhost:8000/docs\n")

        print("🚚 模拟硬件信息:")
        print("   车辆数量: 3")
        print("   上报间隔: 15秒")
        print("   速度: 80 km/h")
        print("   路线: 北京 → 天津")
        print("   模式: 直接数据注入（无需MQTT Broker）\n")

        print("按 Ctrl+C 停止所有服务...\n")

        # 等待中断
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n[中断] 正在停止所有服务...")
        for name, proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print("   ✓ {} 已停止".format(name))
            except:
                try:
                    proc.kill()
                    print("   ✓ {} 已强制停止".format(name))
                except:
                    pass

        print("\n✓ 所有服务已停止\n")

if __name__ == "__main__":
    main()
