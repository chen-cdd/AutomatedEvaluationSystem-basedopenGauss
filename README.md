# Agent 自动化评测系统

这是一个面向外部 Agent 交互日志的自动化评测系统，包含日志导入、脱敏与标准化、轨迹树解析、LLM-as-a-Judge 评分、openGauss/SQLite 持久化，以及面向毕业设计展示的前端看板。

## 技术栈

- 后端：FastAPI + SQLAlchemy
- 数据库：openGauss（生产目标）/ SQLite（默认开发启动）
- 前端：React + Vite
- 评测范式：LLM-as-a-Judge（当前提供 mock judge，可替换真实 API）

## 启动方式

### 后端

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 当前已实现

- JSON 日志上传与批量导入
- 日志脱敏、标准化
- 轨迹树与时间轴重构
- 评测任务异步处理
- 多维评分结果生成
- 任务列表、详情、重跑、删除
- 总览页、统计分析页、BadCase 页面
- openGauss 建表 SQL

## openGauss 切换

修改 `backend/.env` 中的 `DATABASE_URL` 为 openGauss 连接串，并用 `backend/schema.sql` 初始化数据库。
