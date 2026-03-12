#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的系统测试脚本 - 不需要真实MQTT Broker
"""
import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 设置编码
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加backend目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, DeviceLocation, Base, engine
from models import LocationData

def test_database():
    """测试数据库连接和操作"""
    print("\n" + "="*50)
    print("测试 1: 数据库连接和操作")
    print("="*50)

    try:
        # 创建表
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建成功")

        # 测试插入数据
        db = SessionLocal()
        test_location = DeviceLocation(
            device_id="test_device_001",
            latitude=39.9042,
            longitude=116.4074,
            battery=85,
            signal_strength=-65,
            status="active",
            timestamp=datetime.utcnow()
        )
        db.add(test_location)
        db.commit()
        print("✓ 测试数据插入成功")

        # 测试查询
        locations = db.query(DeviceLocation).all()
        print(f"✓ 数据库查询成功，共 {len(locations)} 条记录")

        # 显示数据
        for loc in locations:
            print(f"  - {loc.device_id}: ({loc.latitude}, {loc.longitude})")

        db.close()
        return True

    except Exception as e:
        print(f"✗ 数据库测试失败: {e}")
        return False

def test_models():
    """测试数据模型"""
    print("\n" + "="*50)
    print("测试 2: 数据模型验证")
    print("="*50)

    try:
        # 测试LocationData模型
        data = LocationData(
            device_id="device_001",
            latitude=39.9042,
            longitude=116.4074,
            battery=85,
            signal_strength=-65,
            status="active",
            timestamp=datetime.utcnow()
        )
        print("✓ LocationData模型验证成功")
        print(f"  - 设备ID: {data.device_id}")
        print(f"  - 位置: ({data.latitude}, {data.longitude})")
        print(f"  - 电池: {data.battery}%")
        print(f"  - 信号: {data.signal_strength} dBm")
        return True

    except Exception as e:
        print(f"✗ 模型测试失败: {e}")
        return False

def test_config():
    """测试配置加载"""
    print("\n" + "="*50)
    print("测试 3: 配置加载")
    print("="*50)

    try:
        from config import settings
        print("✓ 配置加载成功")
        print(f"  - MQTT Broker: {settings.mqtt_broker}:{settings.mqtt_port}")
        print(f"  - MQTT主题: {settings.mqtt_topic}")
        print(f"  - 数据库: {settings.database_url}")
        print(f"  - 服务器: {settings.server_host}:{settings.server_port}")
        return True

    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def test_imports():
    """测试所有模块导入"""
    print("\n" + "="*50)
    print("测试 4: 模块导入")
    print("="*50)

    modules = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("paho.mqtt.client", "MQTT客户端"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
    ]

    all_ok = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"[OK] {display_name} 导入成功")
        except ImportError as e:
            print(f"[FAIL] {display_name} 导入失败: {e}")
            all_ok = False

    return all_ok

def test_mqtt_client():
    """测试MQTT客户端配置"""
    print("\n" + "="*50)
    print("测试 5: MQTT客户端配置")
    print("="*50)

    try:
        from mqtt_client import mqtt_client
        print("✓ MQTT客户端初始化成功")
        print(f"  - 客户端ID: {mqtt_client.client._client_id}")
        print(f"  - 状态: {'已连接' if mqtt_client.connected else '未连接'}")
        return True

    except Exception as e:
        print(f"✗ MQTT客户端测试失败: {e}")
        return False

def test_websocket_manager():
    """测试WebSocket管理器"""
    print("\n" + "="*50)
    print("测试 6: WebSocket管理器")
    print("="*50)

    try:
        from websocket_manager import manager
        print("✓ WebSocket管理器初始化成功")
        print(f"  - 活跃连接数: {len(manager.active_connections)}")
        return True

    except Exception as e:
        print(f"✗ WebSocket管理器测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + " "*10 + "智能硬件位置追踪系统 - 后端测试" + " "*8 + "║")
    print("╚" + "="*48 + "╝")

    results = []
    results.append(("模块导入", test_imports()))
    results.append(("配置加载", test_config()))
    results.append(("数据模型", test_models()))
    results.append(("数据库", test_database()))
    results.append(("MQTT客户端", test_mqtt_client()))
    results.append(("WebSocket管理器", test_websocket_manager()))

    # 总结
    print("\n" + "="*50)
    print("测试总结")
    print("="*50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {name}")

    print(f"\n总体: {passed}/{total} 测试通过")

    if passed == total:
        print("\n✓ 所有测试通过！系统已准备就绪。")
        return 0
    else:
        print(f"\n✗ 有 {total - passed} 个测试失败。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
