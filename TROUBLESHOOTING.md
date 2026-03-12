# 地图上没有显示车辆和轨迹 - 故障排除指南

## 问题分析

如果地图上没有显示车辆和轨迹，可能的原因有：

1. **模拟硬件未运行** - 没有数据被发送
2. **后端未接收数据** - MQTT连接失败
3. **WebSocket连接失败** - 前端无法接收实时更新
4. **浏览器缓存** - 需要刷新页面
5. **数据库为空** - 没有历史数据

## 快速诊断

### 方式1: 使用诊断脚本（推荐）

```bash
python diagnose.py
```

这将检查：
- ✓ 后端服务状态
- ✓ 数据库连接
- ✓ 设备数据
- ✓ WebSocket连接
- ✓ 前端应用

### 方式2: 手动检查

#### 1. 检查后端是否运行

```bash
curl http://localhost:8000/health
```

预期输出：
```json
{
  "status": "healthy",
  "mqtt_connected": false,
  "timestamp": "2026-03-12T..."
}
```

#### 2. 检查是否有设备数据

```bash
curl http://localhost:8000/devices
```

预期输出：
```json
[
  {
    "device_id": "vehicle_001",
    "latitude": 39.9042,
    "longitude": 116.4074,
    ...
  }
]
```

#### 3. 检查浏览器控制台

打开浏览器开发者工具 (F12)，查看：
- Console 标签：是否有错误信息
- Network 标签：WebSocket连接是否成功
- Application 标签：是否有缓存问题

## 解决方案

### 问题1: 模拟硬件未运行

**症状**: 后端返回空的设备列表

**解决方案**:

```bash
# 使用改进的直接模拟器（推荐）
cd backend
python simulate_vehicle_direct.py multi 3

# 或使用一键启动脚本
python run_all_direct.py
```

### 问题2: MQTT连接失败

**症状**: 后端日志显示 "MQTT连接失败"

**解决方案**:

如果你想使用真实的MQTT Broker：

```bash
# 安装mosquitto
# Windows (WSL): sudo apt-get install mosquitto
# macOS: brew install mosquitto
# Linux: sudo apt-get install mosquitto

# 启动mosquitto
mosquitto -v
```

或者使用改进的直接模拟器（不需要MQTT）：

```bash
python simulate_vehicle_direct.py multi 3
```

### 问题3: WebSocket连接失败

**症状**: 浏览器控制台显示 "WebSocket连接失败"

**解决方案**:

1. 检查后端是否运行在8000端口
2. 检查防火墙设置
3. 刷新浏览器页面
4. 清除浏览器缓存

```bash
# 检查后端是否运行
curl http://localhost:8000/health
```

### 问题4: 浏览器缓存问题

**症状**: 页面显示但没有数据

**解决方案**:

1. 按 `Ctrl+Shift+Delete` 打开清除缓存对话框
2. 选择 "所有时间"
3. 勾选 "Cookies和其他网站数据"
4. 点击 "清除数据"
5. 刷新页面

或者使用硬刷新：
- Windows/Linux: `Ctrl+Shift+R`
- macOS: `Cmd+Shift+R`

### 问题5: 数据库为空

**症状**: 后端返回空列表，但模拟硬件正在运行

**解决方案**:

1. 检查数据库文件是否存在

```bash
ls -la backend/location_data.db
```

2. 如果不存在，重启后端服务会自动创建

3. 检查数据库中的数据

```bash
cd backend
python -c "
from database import SessionLocal, DeviceLocation
db = SessionLocal()
count = db.query(DeviceLocation).count()
print(f'数据库中有 {count} 条记录')
db.close()
"
```

## 完整的启动流程

### 推荐方式：一键启动（改进版）

```bash
python run_all_direct.py
```

这将自动启动：
1. 后端服务 (FastAPI)
2. 前端应用 (Vue 3)
3. 模拟硬件 (直接数据注入，无需MQTT)

### 分步启动

**终端1 - 启动后端**:
```bash
cd backend
python main.py
```

**终端2 - 启动前端**:
```bash
cd frontend
npm run dev
```

**终端3 - 启动模拟硬件**:
```bash
cd backend
python simulate_vehicle_direct.py multi 3
```

## 验证步骤

### 1. 检查后端日志

后端应该显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. 检查模拟硬件日志

模拟硬件应该显示：
```
启动 3 个车辆直接模拟器...
(不需要MQTT Broker，直接注入数据)

[vehicle_001] 数据已保存: (39.9042, 116.4074) 电池: 100% 信号: -65dBm
[vehicle_002] 数据已保存: (39.9200, 116.4500) 电池: 100% 信号: -65dBm
[vehicle_003] 数据已保存: (39.9400, 116.5000) 电池: 100% 信号: -65dBm
```

### 3. 打开浏览器

访问 http://localhost:5173

应该看到：
- ✓ 地图加载
- ✓ 车辆标记显示
- ✓ 轨迹线显示
- ✓ 左侧车队面板显示车辆列表

## 常见错误信息

### "WebSocket连接失败"

**原因**: 后端未运行或WebSocket端口被占用

**解决**:
```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 如果失败，启动后端
cd backend
python main.py
```

### "无法连接到localhost:8000"

**原因**: 后端未启动或端口被占用

**解决**:
```bash
# 检查端口是否被占用
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# 如果被占用，杀死进程或使用其他端口
```

### "地图加载失败"

**原因**: Leaflet或OpenStreetMap加载失败

**解决**:
1. 检查网络连接
2. 刷新页面
3. 清除浏览器缓存

## 调试技巧

### 查看实时日志

**后端日志**:
```bash
cd backend
python main.py 2>&1 | tee backend.log
```

**前端日志**:
打开浏览器开发者工具 (F12) → Console 标签

### 测试API端点

```bash
# 获取所有设备
curl http://localhost:8000/devices | python -m json.tool

# 获取特定设备历史
curl http://localhost:8000/devices/vehicle_001/history | python -m json.tool

# 检查健康状态
curl http://localhost:8000/health | python -m json.tool
```

### 测试WebSocket

```bash
# 使用wscat工具
npm install -g wscat
wscat -c ws://localhost:8000/ws
```

## 性能优化

如果系统运行缓慢：

1. **减少轨迹点数**
   - 编辑 MapView.vue
   - 修改 `if (latlngs.length > 100)` 为更小的值

2. **增加上报间隔**
   - 编辑 simulate_vehicle_direct.py
   - 修改 `time.sleep(15)` 为更大的值

3. **减少车辆数**
   - 运行 `python simulate_vehicle_direct.py multi 1`

## 获取帮助

如果问题仍未解决：

1. 运行诊断脚本：`python diagnose.py`
2. 查看完整日志
3. 检查浏览器控制台错误
4. 查看 README.md 和 USAGE_GUIDE.md

---

**最后更新**: 2026-03-12
**版本**: 2.0
