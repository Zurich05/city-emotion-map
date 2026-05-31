# Deploy

## 本地开发

后端：

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

前端：

```bash
cd frontend
npm install
npm run dev
```

## Docker Compose

项目已提供后端、前端 Dockerfile 和 `docker-compose.yml`：

```bash
docker compose up --build
```

服务：

- 前端：`http://localhost:5173`
- 后端：`http://localhost:8000`

生产环境必须覆盖：

```env
AUTH_USERNAME=your-admin
AUTH_PASSWORD=strong-password
JWT_SECRET_KEY=long-random-secret
```

当前 Docker Compose 使用 SQLite 数据卷。更高并发生产场景建议迁移到 PostgreSQL + PostGIS，并接入集中日志、反向代理 HTTPS 和监控告警。
