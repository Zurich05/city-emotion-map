# city-emotion-map

城市情绪地图系统是一个前后端分离的城市公开文本情绪分析原型。第一阶段聚焦文本数据，支持模拟采集、文件导入、清洗脱敏、本地规则情感分析、统计、热点识别、地图展示和摘要报告。

## 技术栈

- 后端：Python、FastAPI、SQLAlchemy、SQLite、Pydantic
- 前端：Vue 3、Vite、TypeScript、Element Plus、ECharts、Leaflet、Pinia、Axios

## 启动

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
npm install
npm run dev
```

默认开发登录账号：

```text
admin / admin123
```

生产环境请通过 `.env` 修改 `AUTH_USERNAME`、`AUTH_PASSWORD` 和 `JWT_SECRET_KEY`。

## 演示闭环

1. 通过 `POST /api/import/demo` 导入内置 demo，或通过 `POST /api/crawl/start` 生成模拟数据。
2. 调用 `POST /api/clean/run` 清洗并脱敏。
3. 调用 `POST /api/sentiment/run` 执行情感分析。
4. 打开前端登录后查看仪表盘、地图、分析、数据管理和报告页。

数据管理页也提供 demo 导入、模拟采集、清洗、情感分析、任务日志和样本列表。

## Docker Compose

```bash
docker compose up --build
```

## 合规边界

项目默认仅处理模拟、手动导入、公开或授权数据。微博、小红书、抖音适配器仅保留合规接口结构，不提供绕过登录、验证码、风控或反爬策略的代码。

## 后续扩展

可扩展 PostgreSQL + PostGIS、Redis、Celery、真实授权 API、权限管理、审计日志、大模型情感分析、多模态分析和实时数据流。
