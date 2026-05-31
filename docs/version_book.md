# 版本书

## V0.1 工程骨架

已完成：
- 创建 `city-emotion-map` 前后端分离目录。
- 后端采用 FastAPI、SQLAlchemy、SQLite 分层结构。
- 前端采用 Vue 3、Vite、Element Plus、ECharts、Leaflet。
- 创建实施计划文档。

未实现：
- 尚未接入真实平台授权 API。
- 尚未提供生产级 Docker 镜像。

## V0.2 后端数据闭环

已完成：
- 建立 `raw_posts`、`cleaned_posts`、`sentiment_results`、`area_statistics`、`import_logs` 表。
- 实现文件导入、模拟采集、清洗脱敏、本地规则情感分析、统计、热点、报告接口。
- 内置 82 条 demo JSONL 数据。
- 后端核心单元测试覆盖清洗、脱敏、哈希、情感分析和风险等级。
- 后端 API 冒烟测试覆盖模拟采集、清洗、情感分析、地图点位、统计、热点和报告闭环。

未实现：
- 第三方情感 API 仅预留配置与调用结构，未绑定具体供应商协议。
- 统计表目前作为预留表，接口使用实时查询聚合。

## V0.3 前端展示闭环

已完成：
- 登录页、仪表盘、地图页、分析页、数据管理页、报告页。
- 接入统计卡片、ECharts 图表、Leaflet 点位地图、热点卡片、样本列表。
- 数据管理页支持模拟采集、清洗、情感分析和文件上传入口。

未实现：
- PDF / DOCX 导出按钮仅预留。
- 热力图当前以分层点位表达，尚未加入 Leaflet heat 插件。
- 未实现真实登录权限系统。

## V0.4 文档与交付

已完成：
- README、API、数据库、部署、采集合规文档。
- 本地开发启动说明。

未实现：
- CI/CD、生产监控、权限审计、异步任务队列、Redis 缓存、PostGIS 空间分析。

## V0.5 数据管理增强与热力图

已完成：
- 新增 `POST /api/import/demo`，支持一键导入后端内置 demo 数据。
- 新增 `GET /api/import/logs`，支持查看导入、采集、清洗、情感分析任务日志。
- 修正文件导入 `replace` 清空数据时的 SQLAlchemy 2 写法。
- 数据管理页新增“导入 demo”按钮和任务日志表。
- 地图页接入 `leaflet.heat`，在“压力”和“数据密度”图层显示真实热力层。
- 报告页新增 TXT / DOC 文本下载能力，替代原来的完全禁用导出按钮。
- 本阶段变更已纳入 Git 自动提交与推送流程。

未实现：
- 热力图仍基于点位强度计算，尚未做网格聚合或行政区面聚合。

## V0.6 认证、原生导出与生产部署基础

已完成：
- 新增 `POST /api/auth/login`，通过 JWT Bearer Token 保护写操作接口。
- 文件导入、demo 导入、模拟采集、清洗、情感分析和报告导出接口已启用鉴权。
- 前端登录页接入真实后端登录，后续 API 请求自动携带 token。
- 顶部栏新增退出登录。
- 报告页接入后端原生 PDF / DOCX 导出。
- 后端新增 PDF / DOCX 二进制报告生成。
- 新增后端 `Dockerfile`、前端 `Dockerfile`、Nginx 前端代理配置。
- `docker-compose.yml` 改为 build 模式并使用 SQLite 数据卷。
- 新增 GitHub Actions CI，覆盖后端测试、后端编译和前端构建。
- 本阶段变更已完成测试、提交并推送到 GitHub。

未实现：
- 当前认证是单管理员环境变量账号，尚未实现多用户、角色权限、密码重置和审计后台。
- Docker Compose 仍使用 SQLite，生产高并发建议迁移 PostgreSQL + PostGIS。
- CI 尚未加入镜像构建发布、漏洞扫描和部署流水线。
