# Backend

FastAPI 后端提供数据导入、模拟采集、清洗、情感分析、统计、热点和报告接口。

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

默认数据库为 SQLite，启动时自动初始化表结构。
