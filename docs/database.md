# Database

默认使用 SQLite，ORM 位于 `backend/app/models`。

- `raw_posts`：原始文本、平台、关键词、发布时间、互动数、粗粒度地理信息。
- `cleaned_posts`：清洗文本、城市、区县、地点、脱敏坐标、文本哈希。
- `sentiment_results`：情绪标签、综合分、压力、愉悦、愤怒、平静、模型信息。
- `area_statistics`：预留聚合统计表。
- `import_logs`：导入、采集、清洗、分析任务日志。

迁移到 PostgreSQL + PostGIS 时，可将 `lat/lng` 替换或同步为 `geometry(Point, 4326)`，并为时间、平台、区域、空间字段建立索引。
