#!/usr/bin/env python3
"""
简单的MQTT Broker模拟器 - 用于测试
在实际环境中应使用真实的mosquitto或云MQTT服务
"""
import socket
import threading
import json
import time
from datetime import datetime

class SimpleMQTTBroker:
    def __init__(self, host='localhost', port=1883):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
        self.subscriptions = {}
        self.running = False

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.running = True
        print(f"✓ MQTT Broker启动在 {self.host}:{self.port}")

        while self.running:
            try:
                client, addr = self.server.accept()
                print(f"✓ 客户端连接: {addr}")
                thread = threading.Thread(target=self.handle_client, args=(client, addr))
                thread.daemon = True
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"错误: {e}")

    def handle_client(self, client, addr):
        try:
            while self.running:
                data = client.recv(1024)
                if not data:
                    break

                # 简单的MQTT消息处理
                message = data.decode('utf-8', errors='ignore')
                if 'CONNECT' in message:
                    client.send(b'\x20\x02\x00\x00')  # CONNACK
                    print(f"  → {addr} 已连接")
                elif 'PUBLISH' in message or 'devices/location' in message:
                    print(f"  → 收到消息来自 {addr}")
                elif 'SUBSCRIBE' in message:
                    client.send(b'\x90\x03\x00\x01\x00')  # SUBACK
                    print(f"  → {addr} 已订阅")

        except Exception as e:
            print(f"客户端错误 {addr}: {e}")
        finally:
            client.close()

    def stop(self):
        self.running = False
        if self.server:
            self.server.close()

if __name__ == "__main__":
    broker = SimpleMQTTBroker()
    try:
        broker.start()
    except KeyboardInterrupt:
        print("\n✓ MQTT Broker已停止")
        broker.stop()
