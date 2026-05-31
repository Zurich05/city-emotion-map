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

## Docker

当前提供 `docker-compose.yml` 作为扩展起点。生产部署建议补充独立 Dockerfile、反向代理、日志目录、数据库卷和环境变量管理。
