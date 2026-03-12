#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单诊断脚本 - 检查系统状态
"""
import sys
import os
import requests
import time

sys.path.insert(0, 'backend')

def check_backend():
    """检查后端服务"""
    print("\n[CHECK] Backend Service...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("  OK - Backend is running")
            print(f"    - MQTT connected: {data.get('mqtt_connected')}")
            return True
        else:
            print(f"  FAIL - Backend returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"  FAIL - Backend connection error: {e}")
        return False

def check_database():
    """检查数据库"""
    print("\n[CHECK] Database...")
    try:
        from database import SessionLocal, DeviceLocation
        db = SessionLocal()
        count = db.query(DeviceLocation).count()
        db.close()
        print(f"  OK - Database is working")
        print(f"    - Records: {count}")
        return True
    except Exception as e:
        print(f"  FAIL - Database error: {e}")
        return False

def check_devices():
    """检查设备数据"""
    print("\n[CHECK] Device Data...")
    try:
        response = requests.get('http://localhost:8000/devices', timeout=5)
        if response.status_code == 200:
            devices = response.json()
            print(f"  OK - Got device data")
            print(f"    - Device count: {len(devices)}")
            for device in devices[:3]:
                print(f"    - {device['device_id']}: ({device['latitude']:.4f}, {device['longitude']:.4f})")
            return len(devices) > 0
        else:
            print(f"  FAIL - Got status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  FAIL - Device data error: {e}")
        return False

def check_websocket():
    """检查WebSocket"""
    print("\n[CHECK] WebSocket...")
    try:
        import websocket
        ws = websocket.create_connection("ws://localhost:8000/ws", timeout=5)
        print("  OK - WebSocket connection successful")
        ws.close()
        return True
    except ImportError:
        print("  SKIP - websocket-client not installed")
        return True
    except Exception as e:
        print(f"  FAIL - WebSocket error: {e}")
        return False

def check_frontend():
    """检查前端"""
    print("\n[CHECK] Frontend...")
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("  OK - Frontend is running")
            return True
        else:
            print(f"  FAIL - Frontend returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"  FAIL - Frontend error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("VEHICLE TRACKING SYSTEM - DIAGNOSTIC")
    print("="*60)

    results = []

    # Check components
    results.append(("Backend", check_backend()))
    results.append(("Database", check_database()))
    results.append(("Devices", check_devices()))
    results.append(("WebSocket", check_websocket()))
    results.append(("Frontend", check_frontend()))

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "OK" if result else "FAIL"
        print(f"[{status}] {name}")

    print(f"\nTotal: {passed}/{total} components OK")

    if passed == total:
        print("\nAll systems operational!")
        print("\nIf no vehicles on map:")
        print("  1. Check if simulator is running")
        print("  2. Refresh browser (Ctrl+Shift+R)")
        print("  3. Check browser console (F12)")
        return 0
    else:
        print(f"\n{total - passed} components failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
