# 部署指南 - 智能硬件位置追踪系统

## 目录
1. [本地开发部署](#本地开发部署)
2. [生产环境部署](#生产环境部署)
3. [环境变量配置](#环境变量配置)
4. [故障排查](#故障排查)

## 本地开发部署

### 前置要求
- Docker & Docker Compose
- Git
- Node.js 18+ (如果不使用Docker)
- Python 3.13+ (如果不使用Docker)

### 快速启动

1. **克隆项目**
```bash
git clone <your-repo-url>
cd <project-directory>
```

2. **启动所有服务**
```bash
docker-compose up --build
```

3. **访问应用**
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 首次使用

1. 打开 http://localhost:5173
2. 点击"注册"创建新账户
3. 输入用户名、邮箱和密码
4. 点击"登录"使用新账户登录
5. 系统将显示实时设备位置

### 停止服务
```bash
docker-compose down
```

### 查看日志
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 生产环境部署

### 选项1: 使用Render部署

#### 步骤1: 准备GitHub仓库
1. 将代码推送到GitHub
2. 确保`.env`文件在`.gitignore`中（不要提交敏感信息）

#### 步骤2: 部署后端到Render

1. 访问 https://render.com
2. 点击"New +" → "Web Service"
3. 连接GitHub仓库
4. 配置如下:
   - **Name**: location-tracking-backend
   - **Environment**: Docker
   - **Build Command**: (留空)
   - **Start Command**: (留空)
   - **Root Directory**: backend

5. 在"Environment"标签页添加环境变量:
   ```
   MQTT_BROKER=your-mqtt-broker.com
   MQTT_PORT=8883
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   SECRET_KEY=<生成强密钥>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. 点击"Create Web Service"

#### 步骤3: 部署前端到Render

1. 点击"New +" → "Static Site"
2. 连接GitHub仓库
3. 配置如下:
   - **Name**: location-tracking-frontend
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

4. 在"Environment"标签页添加:
   ```
   VITE_API_URL=https://location-tracking-backend.onrender.com
   ```

5. 点击"Create Static Site"

### 选项2: 使用Railway部署

#### 步骤1: 连接GitHub
1. 访问 https://railway.app
2. 点击"New Project"
3. 选择"Deploy from GitHub repo"
4. 授权并选择你的仓库

#### 步骤2: 配置后端服务
1. 添加PostgreSQL数据库
2. 添加环境变量
3. 配置Dockerfile路径: `backend/Dockerfile`

#### 步骤3: 配置前端服务
1. 添加新服务
2. 配置构建命令: `cd frontend && npm install && npm run build`
3. 配置启动命令: `npm run preview`

### 选项3: 使用自己的服务器

#### 使用Docker Compose
```bash
# 1. 克隆项目
git clone <your-repo-url>
cd <project-directory>

# 2. 创建.env文件
cp .env.example .env
# 编辑.env文件，设置生产环境变量

# 3. 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 4. 配置Nginx反向代理
# 参考下面的Nginx配置
```

#### Nginx配置示例
```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 前端
    location / {
        root /var/www/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws {
        proxy_pass http://backend/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## 环境变量配置

### 后端环境变量

| 变量名 | 说明 | 默认值 | 生产环境建议 |
|--------|------|--------|------------|
| `MQTT_BROKER` | MQTT服务器地址 | localhost | 云MQTT服务地址 |
| `MQTT_PORT` | MQTT端口 | 1883 | 8883 (TLS) |
| `DATABASE_URL` | 数据库连接字符串 | sqlite:///./location_data.db | PostgreSQL URL |
| `SECRET_KEY` | JWT签名密钥 | 默认值 | 强随机密钥 |
| `ALGORITHM` | JWT算法 | HS256 | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 令牌过期时间 | 30 | 30-60 |
| `SERVER_HOST` | 服务器监听地址 | 0.0.0.0 | 0.0.0.0 |
| `SERVER_PORT` | 服务器端口 | 8000 | 8000 |

### 前端环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_API_URL` | 后端API地址 | http://localhost:8000 |

### 生成强密钥
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32
```

## 故障排查

### 后端无法连接MQTT
- 检查MQTT_BROKER和MQTT_PORT配置
- 确保MQTT服务器正在运行
- 检查防火墙设置

### 前端无法连接后端
- 检查VITE_API_URL配置
- 确保后端服务正在运行
- 检查CORS配置
- 查看浏览器控制台错误信息

### 数据库连接错误
- 检查DATABASE_URL格式
- 确保数据库服务正在运行
- 检查数据库凭证

### WebSocket连接失败
- 检查后端WebSocket端点
- 确保代理正确配置WebSocket升级
- 查看浏览器网络标签页

### 认证失败
- 检查SECRET_KEY是否一致
- 确保令牌未过期
- 检查浏览器本地存储中的令牌

## 监控和维护

### 日志查看
```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# 系统日志
tail -f /var/log/location-tracking/backend.log
```

### 数据库备份
```bash
# SQLite
cp location_data.db location_data.db.backup

# PostgreSQL
pg_dump dbname > backup.sql
```

### 性能优化
1. 启用数据库索引
2. 配置Redis缓存
3. 使用CDN分发前端资源
4. 启用Gzip压缩

## 安全建议

1. **更改默认密钥**: 生成强随机密钥替换SECRET_KEY
2. **使用HTTPS**: 在生产环境中强制使用HTTPS
3. **MQTT安全**: 使用TLS加密MQTT连接
4. **数据库安全**: 使用强密码，限制访问权限
5. **定期更新**: 保持依赖包最新
6. **备份数据**: 定期备份数据库
7. **监控日志**: 定期检查错误日志

## 支持

如有问题，请查看:
- 后端API文档: `/docs`
- 项目GitHub Issues
- 系统日志
