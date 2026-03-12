#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统诊断脚本 - 检查所有组件是否正常工作
"""
import sys
import os
import requests
import time
from datetime import datetime

sys.path.insert(0, 'backend')

def check_backend():
    """检查后端服务"""
    print("\n[检查] 后端服务...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("  ✓ 后端服务正常")
            print(f"    - MQTT连接: {'已连接' if data.get('mqtt_connected') else '未连接'}")
            print(f"    - 时间戳: {data.get('timestamp')}")
            return True
        else:
            print(f"  ✗ 后端返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ 后端连接失败: {e}")
        return False

def check_database():
    """检查数据库"""
    print("\n[检查] 数据库...")
    try:
        from database import SessionLocal, DeviceLocation
        db = SessionLocal()
        count = db.query(DeviceLocation).count()
        db.close()
        print(f"  ✓ 数据库正常")
        print(f"    - 记录数: {count}")
        return True
    except Exception as e:
        print(f"  ✗ 数据库错误: {e}")
        return False

def check_devices():
    """检查设备数据"""
    print("\n[检查] 设备数据...")
    try:
        response = requests.get('http://localhost:8000/devices', timeout=5)
        if response.status_code == 200:
            devices = response.json()
            print(f"  ✓ 获取设备数据成功")
            print(f"    - 设备数: {len(devices)}")
            for device in devices:
                print(f"    - {device['device_id']}: ({device['latitude']:.4f}, {device['longitude']:.4f})")
            return len(devices) > 0
        else:
            print(f"  ✗ 获取设备数据失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ 获取设备数据错误: {e}")
        return False

def check_websocket():
    """检查WebSocket"""
    print("\n[检查] WebSocket...")
    try:
        import websocket
        ws = websocket.create_connection("ws://localhost:8000/ws", timeout=5)
        print("  ✓ WebSocket连接成功")
        ws.close()
        return True
    except ImportError:
        print("  ⚠ websocket-client未安装，跳过检查")
        return True
    except Exception as e:
        print(f"  ✗ WebSocket连接失败: {e}")
        return False

def check_frontend():
    """检查前端"""
    print("\n[检查] 前端应用...")
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("  ✓ 前端应用正常")
            return True
        else:
            print(f"  ✗ 前端返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ 前端连接失败: {e}")
        return False

def main():
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║                                                                ║")
    print("║     🚚 运输车队实时追踪系统 - 系统诊断                        ║")
    print("║                                                                ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    results = []

    # 检查各个组件
    results.append(("后端服务", check_backend()))
    results.append(("数据库", check_database()))
    results.append(("设备数据", check_devices()))
    results.append(("WebSocket", check_websocket()))
    results.append(("前端应用", check_frontend()))

    # 总结
    print("\n" + "="*60)
    print("诊断总结")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 正常" if result else "✗ 异常"
        print(f"{status}: {name}")

    print(f"\n总体: {passed}/{total} 组件正常")

    if passed == total:
        print("\n✓ 系统运行正常！")
        print("\n可能的问题:")
        print("  • 如果地图上没有显示车辆，请检查:")
        print("    1. 模拟硬件是否正在运行")
        print("    2. 浏览器是否已刷新")
        print("    3. 浏览器控制台是否有错误")
        return 0
    else:
        print(f"\n✗ 有 {total - passed} 个组件异常")
        print("\n故障排除:")
        print("  1. 检查所有服务是否已启动")
        print("  2. 查看服务日志")
        print("  3. 检查端口是否被占用")
        return 1

if __name__ == "__main__":
    sys.exit(main())
