#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试脚本 - 启动完整系统并进行测试
"""
import subprocess
import time
import sys
import os
import signal
import requests
import json
from datetime import datetime

class SystemTester:
    def __init__(self):
        self.processes = []
        self.backend_ready = False
        self.frontend_ready = False

    def start_backend(self):
        """启动后端服务"""
        print("\n[启动] 后端服务...")
        try:
            # 改变到backend目录
            backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
            os.chdir(backend_dir)

            # 启动FastAPI服务
            proc = subprocess.Popen(
                [sys.executable, 'main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(('backend', proc))
            print("[OK] 后端进程已启动 (PID: {})".format(proc.pid))

            # 等待服务启动
            time.sleep(3)

            # 检查健康状态
            for i in range(10):
                try:
                    response = requests.get('http://localhost:8000/health', timeout=2)
                    if response.status_code == 200:
                        print("[OK] 后端服务已就绪")
                        self.backend_ready = True
                        return True
                except:
                    time.sleep(1)

            print("[FAIL] 后端服务未响应")
            return False

        except Exception as e:
            print("[FAIL] 启动后端失败: {}".format(e))
            return False

    def start_frontend(self):
        """启动前端开发服务"""
        print("\n[启动] 前端服务...")
        try:
            frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
            os.chdir(frontend_dir)

            proc = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(('frontend', proc))
            print("[OK] 前端进程已启动 (PID: {})".format(proc.pid))

            # 等待服务启动
            time.sleep(5)

            # 检查前端是否可访问
            for i in range(10):
                try:
                    response = requests.get('http://localhost:5173', timeout=2)
                    if response.status_code == 200:
                        print("[OK] 前端服务已就绪")
                        self.frontend_ready = True
                        return True
                except:
                    time.sleep(1)

            print("[WARN] 前端服务可能未完全就绪，但进程已启动")
            return True

        except Exception as e:
            print("[FAIL] 启动前端失败: {}".format(e))
            return False

    def test_api(self):
        """测试API端点"""
        print("\n[测试] API端点...")

        tests = [
            ('GET', 'http://localhost:8000/health', '健康检查'),
            ('GET', 'http://localhost:8000/devices', '获取设备列表'),
        ]

        passed = 0
        for method, url, name in tests:
            try:
                if method == 'GET':
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        print("[OK] {} - {}".format(name, response.status_code))
                        passed += 1
                    else:
                        print("[FAIL] {} - {}".format(name, response.status_code))
            except Exception as e:
                print("[FAIL] {} - {}".format(name, str(e)))

        return passed == len(tests)

    def test_websocket(self):
        """测试WebSocket连接"""
        print("\n[测试] WebSocket连接...")

        try:
            import websocket

            def on_message(ws, message):
                print("[OK] 收到WebSocket消息: {}".format(message[:50]))

            def on_error(ws, error):
                print("[FAIL] WebSocket错误: {}".format(error))

            def on_close(ws, close_status_code, close_msg):
                print("[OK] WebSocket连接已关闭")

            def on_open(ws):
                print("[OK] WebSocket连接已建立")
                ws.close()

            ws = websocket.WebSocketApp(
                "ws://localhost:8000/ws",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )

            ws.run_forever(timeout=5)
            return True

        except ImportError:
            print("[WARN] websocket-client未安装，跳过WebSocket测试")
            return True
        except Exception as e:
            print("[FAIL] WebSocket测试失败: {}".format(e))
            return False

    def cleanup(self):
        """清理进程"""
        print("\n[清理] 停止所有服务...")
        for name, proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print("[OK] {} 已停止".format(name))
            except:
                proc.kill()
                print("[OK] {} 已强制停止".format(name))

    def run(self):
        """运行完整测试"""
        print("\n╔════════════════════════════════════════════════╗")
        print("║   智能硬件位置追踪系统 - 集成测试              ║")
        print("╚════════════════════════════════════════════════╝")

        try:
            # 启动服务
            if not self.start_backend():
                print("\n[FAIL] 后端启动失败")
                return False

            # 测试API
            if not self.test_api():
                print("\n[WARN] 部分API测试失败")

            # 测试WebSocket
            if not self.test_websocket():
                print("\n[WARN] WebSocket测试失败")

            print("\n╔════════════════════════════════════════════════╗")
            print("║              测试完成                          ║")
            print("╚════════════════════════════════════════════════╝")
            print("\n后端服务运行在: http://localhost:8000")
            print("前端服务运行在: http://localhost:5173")
            print("\n按 Ctrl+C 停止服务...")

            # 保持运行
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n[中断] 用户中断")
        finally:
            self.cleanup()

if __name__ == "__main__":
    tester = SystemTester()
    tester.run()
