# Windows 启动指南

## 推荐方式1：使用批处理脚本（最简单）

双击运行：
```
start_direct.bat
```

这将自动打开3个窗口：
1. 后端服务窗口
2. 前端服务窗口
3. 模拟硬件窗口

然后在浏览器打开：
```
http://localhost:5173
```

## 推荐方式2：使用改进的Python脚本

在PowerShell或CMD中运行：
```powershell
python run_all_direct_v2.py
```

## 方式3：手动启动（分步）

### 步骤1：启动后端

打开PowerShell或CMD，运行：
```powershell
cd backend
python main.py
```

预期输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 步骤2：启动前端

打开新的PowerShell或CMD窗口，运行：
```powershell
cd frontend
npm run dev
```

预期输出：
```
VITE v5.0.8  ready in 123 ms
➜  Local:   http://localhost:5173/
```

### 步骤3：启动模拟硬件

打开第三个PowerShell或CMD窗口，运行：
```powershell
cd backend
python simulate_vehicle_direct.py multi 3
```

预期输出：
```
启动 3 个车辆直接模拟器...
(不需要MQTT Broker，直接注入数据)

[vehicle_001] 数据已保存: (39.9042, 116.4074) 电池: 100% 信号: -65dBm
[vehicle_002] 数据已保存: (39.9200, 116.4500) 电池: 100% 信号: -65dBm
[vehicle_003] 数据已保存: (39.9400, 116.5000) 电池: 100% 信号: -65dBm
```

## 访问应用

启动所有服务后，在浏览器打开：

```
http://localhost:5173
```

应该看到：
- ✓ 地图加载
- ✓ 3个彩色车辆标记（🚚）
- ✓ 虚线轨迹显示
- ✓ 左侧车队面板
- ✓ 实时位置更新

## 停止服务

### 方式1：关闭窗口
- 直接关闭后端、前端、模拟硬件窗口

### 方式2：使用Ctrl+C
- 在每个窗口中按 Ctrl+C 停止服务

### 方式3：使用任务管理器
- 按 Ctrl+Shift+Esc 打开任务管理器
- 搜索 "python" 或 "node"
- 右键点击 → 结束任务

## 常见问题

### 问题1：npm命令找不到

**症状**:
```
'npm' 不是内部或外部命令
```

**解决**:
1. 确保Node.js已安装
2. 重启PowerShell或CMD
3. 运行 `npm --version` 验证

### 问题2：Python找不到

**症状**:
```
'python' 不是内部或外部命令
```

**解决**:
1. 确保Python已安装
2. 使用完整路径：`C:\Users\isonu\AppData\Local\Programs\Python\Python313\python.exe`
3. 或者使用 `python.exe` 代替 `python`

### 问题3：端口被占用

**症状**:
```
Address already in use
```

**解决**:
1. 关闭其他使用这些端口的应用
2. 或者修改端口号

### 问题4：地图上没有显示车辆

**症状**:
- 地图加载但没有车辆标记

**解决**:
1. 检查模拟硬件窗口是否有错误
2. 刷新浏览器（Ctrl+Shift+R）
3. 检查浏览器控制台（F12）是否有错误

## 诊断系统

运行诊断脚本检查系统状态：

```powershell
python diagnose.py
```

## 快速参考

| 任务 | 命令 |
|------|------|
| 一键启动 | `python run_all_direct_v2.py` |
| 批处理启动 | `start_direct.bat` |
| 启动后端 | `cd backend && python main.py` |
| 启动前端 | `cd frontend && npm run dev` |
| 启动模拟硬件 | `cd backend && python simulate_vehicle_direct.py multi 3` |
| 诊断系统 | `python diagnose.py` |
| 访问应用 | http://localhost:5173 |

---

**版本**: 2.1
**最后更新**: 2026-03-12
**状态**: 生产就绪 ✓
