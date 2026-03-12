#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运输车模拟器 - 生成合理的运输车轨迹
速度: 80 km/h
上报间隔: 15秒
"""
import paho.mqtt.client as mqtt
import json
import time
import math
from datetime import datetime
from config import settings

class VehicleSimulator:
    def __init__(self, vehicle_id="vehicle_001"):
        self.vehicle_id = vehicle_id
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=f"simulator_{vehicle_id}")
        self.connected = False

        # 初始位置（北京市中心）
        self.latitude = 39.9042
        self.longitude = 116.4074

        # 速度: 80 km/h = 80000 m/h = 22.22 m/s
        # 15秒间隔: 22.22 * 15 = 333.3 米
        # 1度约111km，所以1度约0.00009度/米
        self.speed_kmh = 80
        self.interval = 15  # 秒
        self.distance_per_update = (self.speed_kmh * 1000) / 3600 * self.interval  # 米

        # 轨迹路线（模拟从北京到天津的运输路线）
        self.route_points = self.generate_route()
        self.current_point_index = 0
        self.current_progress = 0  # 当前点到下一个点的进度 (0-1)

        self.battery = 100
        self.signal_strength = -65

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def generate_route(self):
        """生成从北京到天津的合理运输路线"""
        # 北京市中心 -> 天津市中心 (约120km)
        # 使用多个中间点模拟真实路线
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

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.vehicle_id}] 已连接到MQTT Broker")
            self.connected = True
        else:
            print(f"[{self.vehicle_id}] 连接失败，代码: {rc}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"[{self.vehicle_id}] 意外断开连接")
        self.connected = False

    def connect(self):
        """连接到MQTT Broker"""
        try:
            self.client.connect(settings.mqtt_broker, settings.mqtt_port, keepalive=60)
            self.client.loop_start()
            time.sleep(1)
        except Exception as e:
            print(f"[{self.vehicle_id}] 连接失败: {e}")

    def publish_location(self):
        """发布位置数据"""
        self.get_next_position()

        payload = {
            "device_id": self.vehicle_id,
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6),
            "battery": int(self.battery),
            "signal_strength": int(self.signal_strength),
            "status": "active",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        topic = f"devices/location/{self.vehicle_id}"
        self.client.publish(topic, json.dumps(payload))
        print(f"[{self.vehicle_id}] 发布位置: ({payload['latitude']:.4f}, {payload['longitude']:.4f}) "
              f"电池: {payload['battery']}% 信号: {payload['signal_strength']}dBm")

    def run(self, duration=None):
        """运行模拟器"""
        self.connect()
        start_time = time.time()

        try:
            while True:
                if duration and (time.time() - start_time) > duration:
                    break

                self.publish_location()
                time.sleep(self.interval)

        except KeyboardInterrupt:
            print(f"\n[{self.vehicle_id}] 模拟器已停止")
        finally:
            self.client.loop_stop()
            self.client.disconnect()

    def stop(self):
        """停止模拟器"""
        self.client.loop_stop()
        self.client.disconnect()


class MultiVehicleSimulator:
    """多车辆模拟器"""
    def __init__(self, num_vehicles=3):
        self.simulators = []
        for i in range(num_vehicles):
            vehicle_id = f"vehicle_{i+1:03d}"
            simulator = VehicleSimulator(vehicle_id)
            self.simulators.append(simulator)

    def start(self):
        """启动所有模拟器"""
        print(f"启动 {len(self.simulators)} 个车辆模拟器...")
        for simulator in self.simulators:
            simulator.connect()

        try:
            while True:
                for simulator in self.simulators:
                    simulator.publish_location()
                time.sleep(15)

        except KeyboardInterrupt:
            print("\n所有模拟器已停止")
        finally:
            for simulator in self.simulators:
                simulator.stop()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "multi":
        # 多车辆模式
        num_vehicles = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        simulator = MultiVehicleSimulator(num_vehicles)
        simulator.start()
    else:
        # 单车辆模式
        vehicle_id = sys.argv[1] if len(sys.argv) > 1 else "vehicle_001"
        simulator = VehicleSimulator(vehicle_id)
        simulator.run()
