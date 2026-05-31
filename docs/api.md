# API

所有接口返回：

```json
{ "code": 0, "message": "success", "data": {}, "meta": {} }
```

- `GET /api/health`：健康检查。
- `POST /api/auth/login`：登录获取 Bearer Token，默认开发账号由 `.env` 中 `AUTH_USERNAME`、`AUTH_PASSWORD` 配置。
- `GET /api/users`：管理员查看用户列表。
- `POST /api/users`：管理员创建用户，角色支持 `admin`、`analyst`、`viewer`。
- `PATCH /api/users/{id}`：管理员修改用户角色、启用状态或密码。
- `POST /api/import`：上传 JSON、JSONL、CSV，参数 `file`、`platform`、`replace`。
- `POST /api/import/demo`：导入后端内置 demo 数据。
- `GET /api/import/logs`：查看导入、采集、清洗、分析任务日志。
- `GET /api/import/logs?task_type=&platform=&status=&limit=&offset=`：按任务类型、平台、状态分页筛选任务日志。
- `POST /api/crawl/start`：模拟采集，参数 `platform`、`keyword`、`limit`。
- `POST /api/clean/run`：批量清洗未处理原始文本。
- `POST /api/sentiment/run`：批量分析未分析清洗文本。
- `GET /api/emotions`：返回地图点位，支持 `platform`、`city`、`district`、`emotion_type`。
- `GET /api/statistics/overview`：概览指标。
- `GET /api/statistics/platform`：平台统计。
- `GET /api/statistics/timeline`：时间趋势。
- `GET /api/statistics/district-rank`：区域排名。
- `GET /api/hotspots`：热点区域与治理建议。
- `GET /api/report`：摘要报告。
- `GET /api/report/export?format=pdf`：导出 PDF 报告，需要 Bearer Token。
- `GET /api/report/export?format=docx`：导出 DOCX 报告，需要 Bearer Token。
- `GET /api/audit/logs`：查看受保护接口操作审计日志，需要 Bearer Token。
- `GET /api/audit/logs?method=&path=&username=&limit=&offset=`：按方法、路径前缀、用户分页筛选审计日志，需要 Bearer Token。
- `GET /api/backup/export`：导出 JSON 数据备份，需要 Bearer Token。
- `POST /api/backup/restore`：上传 JSON 备份并恢复数据，需要 Bearer Token，表单参数 `file`、`replace`。

以下写操作接口需要 `Authorization: Bearer <token>`：

- `POST /api/import`
- `POST /api/import/demo`
- `POST /api/crawl/start`
- `POST /api/clean/run`
- `POST /api/sentiment/run`
- `GET /api/report/export`
- `GET /api/audit/logs`
- `GET /api/backup/export`
- `POST /api/backup/restore`
