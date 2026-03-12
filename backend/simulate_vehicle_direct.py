#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接数据注入模拟器 - 不依赖MQTT Broker
直接将数据存储到数据库并通过WebSocket推送
"""
import asyncio
import json
import time
import math
from datetime import datetime
from database import SessionLocal, DeviceLocation
from websocket_manager import manager

class DirectVehicleSimulator:
    """直接模拟器 - 不需要MQTT Broker"""
    def __init__(self, vehicle_id="vehicle_001"):
        self.vehicle_id = vehicle_id

        # 初始位置（北京市中心）
        self.latitude = 39.9042
        self.longitude = 116.4074

        # 速度: 80 km/h = 80000 m/h = 22.22 m/s
        # 15秒间隔: 22.22 * 15 = 333.3 米
        self.speed_kmh = 80
        self.interval = 15  # 秒
        self.distance_per_update = (self.speed_kmh * 1000) / 3600 * self.interval  # 米

        # 轨迹路线（模拟从北京到天津的运输路线）
        self.route_points = self.generate_route()
        self.current_point_index = 0
        self.current_progress = 0  # 当前点到下一个点的进度 (0-1)

        self.battery = 100
        self.signal_strength = -65

    def generate_route(self):
        """生成从北京到天津的合理运输路线"""
        route = [
            (39.9042, 116.4074),   # 北京市中心
            (39.9200, 116.4500),   # 向东北方向
            (39.9400, 116.5000),   # 继续东北
            (39.9600, 116.5500),   # 进入郊区
            (40.0000, 116.6500),   # 向北
            (40.0500, 116.7500),   # 继续北上
            (40.1000, 116.8500),   # 接近天津
            (40.1500, 116.9500),   # 进入天津
            (39.0842, 117.2010),   # 天津市中心
        ]
        return route

    def get_next_position(self):
        """获取下一个位置"""
        if self.current_point_index >= len(self.route_points) - 1:
            # 到达终点，重新开始
            self.current_point_index = 0
            self.current_progress = 0

        current = self.route_points[self.current_point_index]
        next_point = self.route_points[self.current_point_index + 1]

        # 计算两点之间的距离（简化计算）
        lat_diff = next_point[0] - current[0]
        lon_diff = next_point[1] - current[1]
        distance = math.sqrt(lat_diff**2 + lon_diff**2) * 111000  # 转换为米

        # 计算需要多少步到达下一个点
        steps_needed = distance / self.distance_per_update

        # 更新进度
        self.current_progress += 1 / steps_needed

        if self.current_progress >= 1:
            # 移动到下一个点
            self.current_point_index += 1
            self.current_progress = 0
            if self.current_point_index >= len(self.route_points) - 1:
                self.current_point_index = 0

        # 线性插值计算当前位置
        current = self.route_points[self.current_point_index]
        next_point = self.route_points[self.current_point_index + 1]

        self.latitude = current[0] + (next_point[0] - current[0]) * self.current_progress
        self.longitude = current[1] + (next_point[1] - current[1]) * self.current_progress

        # 模拟电池消耗
        self.battery = max(20, 100 - (self.current_point_index / len(self.route_points)) * 80)

        # 模拟信号强度变化
        self.signal_strength = -65 + int(math.sin(time.time() / 10) * 10)

    def publish_location(self):
        """同步发布位置数据到数据库和WebSocket"""
        self.get_next_position()

        # 保存到数据库
        db = SessionLocal()
        try:
            location = DeviceLocation(
                device_id=self.vehicle_id,
                latitude=round(self.latitude, 6),
                longitude=round(self.longitude, 6),
                battery=int(self.battery),
                signal_strength=int(self.signal_strength),
                status="active",
                timestamp=datetime.utcnow()
            )
            db.add(location)
            db.commit()
            print(f"[{self.vehicle_id}] 数据已保存: ({location.latitude:.4f}, {location.longitude:.4f}) "
                  f"电池: {location.battery}% 信号: {location.signal_strength}dBm")
        except Exception as e:
            print(f"[{self.vehicle_id}] 数据库错误: {e}")
            db.rollback()
        finally:
            db.close()

    def run(self):
        """运行模拟器"""
        try:
            while True:
                self.publish_location()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f"\n[{self.vehicle_id}] 模拟器已停止")


class MultiDirectVehicleSimulator:
    """多车辆直接模拟器"""
    def __init__(self, num_vehicles=3):
        self.simulators = []
        for i in range(num_vehicles):
            vehicle_id = f"vehicle_{i+1:03d}"
            simulator = DirectVehicleSimulator(vehicle_id)
            self.simulators.append(simulator)

    def start(self):
        """启动所有模拟器"""
        print(f"\n启动 {len(self.simulators)} 个车辆直接模拟器...")
        print("(不需要MQTT Broker，直接注入数据)\n")

        try:
            while True:
                for simulator in self.simulators:
                    simulator.publish_location()
                time.sleep(15)

        except KeyboardInterrupt:
            print("\n所有模拟器已停止")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "multi":
        # 多车辆模式
        num_vehicles = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        simulator = MultiDirectVehicleSimulator(num_vehicles)
        simulator.start()
    else:
        # 单车辆模式
        vehicle_id = sys.argv[1] if len(sys.argv) > 1 else "vehicle_001"
        simulator = DirectVehicleSimulator(vehicle_id)
        simulator.run()
