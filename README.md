# 基于 openGauss 的 Agent 自动化评测系统

这是一个面向外部 Agent 交互日志的自动化评测系统，也是我的毕业设计项目原型。系统围绕“日志导入 -> 轨迹解析 -> 智能评分 -> 结果存储 -> 可视化分析”构建完整闭环，用于辅助开发者评估大语言模型 Agent 在多轮任务中的执行质量、逻辑连贯性、工具调用效率与安全性。

## 项目背景

随着大语言模型从生成式 AI 逐步演进到 Agentic AI，智能体已经不再只是“回答问题”，而是能够围绕目标进行规划、调用工具、执行任务并产生完整的交互轨迹。与能力快速发展相对的是，Agent 评测体系仍然薄弱，传统依赖人工抽检的方式成本高、效率低、可复现性差。

本项目尝试以 `LLM-as-a-Judge` 为核心范式，构建一个可复用、可扩展、可视化的 Agent 自动化评测系统，并结合 `openGauss` 实现结构化结果存储与统计分析，为毕业设计后续论文撰写和系统演示提供工程基础。

## 系统目标

本系统当前聚焦以下目标：

- 导入外部 Agent 产生的 JSON 交互日志
- 对原始日志进行脱敏、清洗与标准化处理
- 将线性执行日志重构为树状轨迹与时间轴视图
- 通过 LLM-as-a-Judge 范式输出多维评分和自然语言评语
- 使用 openGauss / SQLite 存储任务、评分与统计结果
- 通过前端看板展示任务状态、能力画像、统计结果与 BadCase

## 系统架构

系统采用前后端分离的 B/S 架构，整体可以分为三层：

### 1. 表现层

负责用户交互与可视化展示：

- 任务总览看板
- 日志上传页面
- 任务管理页面
- 任务详情与轨迹树回放
- 统计分析页面
- BadCase 分析页面

### 2. 业务逻辑层

负责核心评测流程：

- 日志上传与任务创建
- 日志脱敏与标准化
- Action / Observation 轨迹解析
- Judge Prompt 构建
- 多维度评分生成
- 异步任务执行与结果回写

### 3. 数据存储层

负责结果持久化与查询：

- `openGauss`：目标正式数据库，用于存储结构化任务与评分数据
- `SQLite`：当前默认开发数据库，方便本地快速运行
- 本地文件存储：保存原始日志和示例样本

## 当前功能

当前版本已经实现一版可演示 MVP，包含以下能力：

- JSON 日志上传与批量导入
- 上传文件格式校验
- 日志脱敏与标准化处理
- 轨迹树与时间轴重构
- 多维评分结果生成
- CoT 风格评分说明
- 任务列表查询、任务详情查看
- 任务重跑与删除
- 仪表盘总览与统计分析
- BadCase 页面展示
- openGauss 建表 SQL 输出

## 技术栈

### 后端

- FastAPI
- SQLAlchemy 2.x
- Pydantic
- Uvicorn

### 前端

- React
- Vite
- React Router

### 数据存储

- openGauss
- SQLite
- JSON 文件存储

### 智能评测

- LLM-as-a-Judge
- Rubrics 多维评分
- Chain of Thought 风格解释输出
- 当前默认使用 mock judge，便于本地联调与毕业设计演示

## 目录结构

```text
backend/
  app/
    api/           # FastAPI 路由
    core/          # 配置、异常处理、日志
    db/            # 数据库连接与基类
    models/        # ORM 模型
    schemas/       # Pydantic 数据结构
    services/      # 日志处理、轨迹解析、评分、任务执行
    utils/         # 文件工具
  storage/
    logs/          # 上传日志存储
    samples/       # 示例评测日志
  schema.sql       # openGauss 建表 SQL
  requirements.txt
frontend/
  src/
    api/           # 前端请求封装
    components/    # 通用组件
    pages/         # 页面
    styles/        # 样式文件
docs/
  development-checklist.md
```

## 快速启动

### 1. 启动后端

```bash
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```

后端默认地址：`http://127.0.0.1:8000`

接口文档：`http://127.0.0.1:8000/docs`

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

## openGauss 使用说明

当前项目默认使用 SQLite 作为开发环境数据库，方便本地快速启动。如果要切换为 openGauss：

1. 修改 `backend/.env` 中的 `DATABASE_URL`
2. 使用 `backend/schema.sql` 初始化数据表
3. 重启后端服务

推荐连接串格式：

```text
DATABASE_URL=postgresql+psycopg2://gaussdb:password@localhost:5432/agent_eval
```

## 示例测试日志

项目提供了示例评测日志，可用于前端上传测试：

- [demo_upload_trace.json](/f:/GraduationProject-weiduo/AutomatedEvaluationSystem-basedopenGauss/backend/storage/samples/demo_upload_trace.json)
- [sample_trace.json](/f:/GraduationProject-weiduo/AutomatedEvaluationSystem-basedopenGauss/backend/storage/samples/sample_trace.json)

## 当前开发进度

从毕业设计整体目标来看，项目目前大致处于“中期可演示版本”阶段：

- 基础工程与前后端联调：已完成
- 核心评测流程 MVP：已完成
- 可视化页面原型：已完成
- openGauss 正式联调：待完善
- 真实 LLM API 接入：待完善
- 自动化测试与性能验证：待完善
- 论文图表与答辩材料整理：待完善

## 下一步计划

后续准备重点补齐以下内容：

- 将 mock judge 替换为真实 GPT / DeepSeek 等模型接口
- 完成 openGauss 数据库联调与持久化验证
- 增加真实 benchmark 日志样例
- 增加更完整的筛选、模型管理和统计分析能力
- 补充测试用例、性能验证与论文插图材料

## 仓库说明

本仓库当前主要服务于毕业设计开发与阶段性演示，后续会随着系统完善逐步补充：

- 更完整的后端异常处理与任务队列能力
- 更细粒度的评分策略
- 更正式的系统部署说明
- 论文相关图示与测试结果
