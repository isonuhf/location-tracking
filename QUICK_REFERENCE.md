# 快速参考指南

## 本地开发

### 启动应用
```bash
docker-compose up --build
```

### 访问地址
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- MQTT: localhost:1883

### 停止应用
```bash
docker-compose down
```

### 查看日志
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mosquitto
```

## 用户认证

### 注册新用户
1. 访问 http://localhost:5173
2. 点击"注册"标签
3. 输入用户名、邮箱、密码
4. 点击"注册"按钮

### 登录
1. 输入用户名和密码
2. 点击"登录"按钮
3. 系统自动保存令牌

### 登出
1. 点击右上角用户名旁的"登出"按钮
2. 返回登录页面

## API端点

### 认证
- `POST /auth/register` - 注册用户
- `POST /auth/login` - 登录用户
- `GET /auth/me` - 获取当前用户

### 设备
- `GET /devices` - 获取所有设备最新位置
- `GET /devices/{device_id}/history` - 获取设备历史位置

### 其他
- `GET /health` - 健康检查
- `GET /docs` - API文档

## 环境变量

### 后端 (.env)
```
MQTT_BROKER=localhost
MQTT_PORT=1883
DATABASE_URL=sqlite:///./location_data.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 前端 (.env)
```
VITE_API_URL=http://localhost:8000
```

## 部署

### Render部署
1. 推送代码到GitHub
2. 在Render创建Web Service (后端)
3. 在Render创建Static Site (前端)
4. 配置环境变量
5. 部署完成

### Railway部署
1. 连接GitHub仓库
2. 添加PostgreSQL
3. 配置环境变量
4. 部署完成

### 自托管
```bash
# 1. 克隆项目
git clone <repo-url>

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 3. 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 4. 配置Nginx反向代理
# 参考 README_DEPLOYMENT.md
```

## 常见问题

### 无法连接MQTT
- 检查MQTT_BROKER配置
- 确保mosquitto容器运行中
- 查看日志: `docker-compose logs mosquitto`

### 前端无法连接后端
- 检查VITE_API_URL配置
- 确保后端服务运行中
- 查看浏览器控制台错误

### 登录失败
- 检查用户名和密码
- 确保数据库已初始化
- 查看后端日志

### 数据库错误
- 检查DATABASE_URL格式
- 确保数据库服务运行中
- 删除旧数据库文件重新初始化

## 文件结构

```
project/
├── backend/
│   ├── main.py              # FastAPI应用
│   ├── auth.py              # 认证模块
│   ├── database.py          # 数据库配置
│   ├── models.py            # 数据模型
│   ├── config.py            # 配置文件
│   ├── mqtt_client.py       # MQTT客户端
│   ├── websocket_manager.py # WebSocket管理
│   ├── requirements.txt     # Python依赖
│   └── Dockerfile           # Docker配置
├── frontend/
│   ├── src/
│   │   ├── App.vue          # 主应用
│   │   ├── main.js          # 入口文件
│   │   ├── views/
│   │   │   └── AuthView.vue # 认证页面
│   │   ├── components/
│   │   │   ├── MapView.vue  # 地图组件
│   │   │   └── DevicePanel.vue # 设备面板
│   │   ├── services/
│   │   │   ├── auth.js      # 认证服务
│   │   │   └── websocket.js # WebSocket服务
│   │   ├── stores/
│   │   │   ├── authStore.js # 认证状态
│   │   │   └── deviceStore.js # 设备状态
│   │   └── router/
│   │       └── index.js     # 路由配置
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml       # Docker编排
├── .env.example             # 环境变量模板
├── .gitignore               # Git忽略
├── README_DEPLOYMENT.md     # 部署指南
├── DEPLOYMENT_CHECKLIST.md  # 检查清单
└── IMPLEMENTATION_SUMMARY.md # 实现总结
```

## 性能优化

### 前端
- 启用Gzip压缩
- 使用CDN分发资源
- 代码分割和懒加载
- 图片优化和压缩

### 后端
- 数据库索引优化
- 查询优化
- 缓存策略
- 连接池配置

### 数据库
- 定期清理旧数据
- 备份和恢复
- 性能监控
- 索引维护

## 安全建议

1. **更改默认密钥**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **使用HTTPS**
   - 生产环境强制HTTPS
   - 配置SSL证书

3. **MQTT安全**
   - 使用TLS加密
   - 配置用户认证

4. **数据库安全**
   - 使用强密码
   - 限制访问权限
   - 定期备份

5. **定期更新**
   - 更新依赖包
   - 安全补丁
   - 代码审计

## 监控和告警

### 日志监控
```bash
# 查看实时日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
```

### 性能监控
- 监控CPU使用率
- 监控内存使用率
- 监控磁盘空间
- 监控网络流量

### 告警设置
- 错误日志告警
- 性能告警
- 磁盘空间告警
- 服务宕机告警

## 备份和恢复

### 数据库备份
```bash
# SQLite
cp location_data.db location_data.db.backup

# PostgreSQL
pg_dump dbname > backup.sql
```

### 恢复
```bash
# SQLite
cp location_data.db.backup location_data.db

# PostgreSQL
psql dbname < backup.sql
```

## 故障排查

### 应用无法启动
1. 检查Docker是否运行
2. 查看构建日志
3. 检查端口是否被占用
4. 查看容器日志

### 性能问题
1. 检查数据库查询
2. 分析API响应时间
3. 检查WebSocket连接
4. 优化前端资源

### 数据丢失
1. 检查备份
2. 恢复数据库
3. 验证数据完整性
4. 更新备份策略

## 联系支持

- 查看API文档: http://localhost:8000/docs
- 查看项目日志
- 检查GitHub Issues
- 查看部署指南

## 有用的命令

```bash
# Docker相关
docker-compose up -d              # 后台启动
docker-compose down               # 停止并删除容器
docker-compose logs -f            # 查看日志
docker-compose ps                 # 查看容器状态
docker-compose exec backend bash  # 进入容器

# 数据库相关
sqlite3 location_data.db          # 打开SQLite数据库
.tables                           # 查看表
SELECT * FROM users;              # 查询用户

# 前端相关
npm install                       # 安装依赖
npm run dev                       # 开发模式
npm run build                     # 生产构建
npm run preview                   # 预览构建

# 后端相关
pip install -r requirements.txt   # 安装依赖
python main.py                    # 运行应用
uvicorn main:app --reload        # 开发模式
```
