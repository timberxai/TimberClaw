# TimberClaw-code

> 基于 [OpenHands](https://github.com/All-Hands-AI/OpenHands) fork 改造的工业业务系统 Builder。
>
> 让工厂信息化负责人从业务场景对话出发，先生成并确认 spec，再在受约束的模板底座内自动生成系统，在 Preview 中体验和反馈，在人工把关下发布到 Prod，最终由不懂代码的车间 / 排产 / 质检人员日常使用。

---

## 仓库身份

- **这是什么**：OpenHands 的一个 fork，TimberClaw-code 的 monorepo
- **目标**：产出一个能够为离散制造工厂生成轻量 MES / BI 系统的 Builder
- **上游**：<https://github.com/All-Hands-AI/OpenHands>（MIT 协议）
- **TimberClaw 工作主分支**：`cursor`（日常开发与 PR 合并目标；请勿直推）
- **`main`**：保留用于上游 / 发布对齐；功能迭代请走 `cursor`

本 README 是 `timberclaw/` 子目录的入口。仓库顶层的 [`README.md`](../README.md) 是 TimberClaw-code 整个项目的门面，按需回看。上游 OpenHands 原始的开发指南仍保留在根 [`AGENTS.md`](../AGENTS.md) 和 [`Development.md`](../Development.md) 等文件里，作为开发环境参考。

---

## 文档入口（阅读顺序）

所有 TimberClaw-code 的产品与工程文档都在本目录下，按下面的顺序阅读：

| 顺序 | 文档 | 读者 | 内容 |
|------|------|------|------|
| 1 | [`docs/PRD.md`](docs/PRD.md) | 所有角色 | **单一真相源**。产品定义、角色、流程、默认实现、MVP 范围、成功标准 |
| 2 | [`AGENTS.md`](AGENTS.md) | Coding Agent / Human Developer | **Coding Agent 工作指南**（必读）：要做什么、不能做什么、怎么挑工单、怎么处理失败 |
| 3 | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) | 所有角色 | 仓库约定：目录纪律、分支命名、commit 规范、上游同步 |
| 4 | [`docs/BACKLOG.md`](docs/BACKLOG.md) | Coding Agent / Platform Engineer | 里程碑 M0–M8 + 50+ 张工单（含验收标准） |
| 5 | [`docs/FORK_CANDIDATES.md`](docs/FORK_CANDIDATES.md) | 参考档案 | 为什么选 OpenHands |

如果这是你第一次进入项目，建议按 1 → 2 → 3 → 4 读一遍再开始写代码。

---

## 当前状态

| 项 | 状态 |
|----|------|
| PRD | **V1.5**（对齐离散制造真实场景 + 概念隔离 + 仪表盘一等公民 + CSV 主数据 + 双视图） |
| BACKLOG | **V1.2**（对齐 PRD V1.5，新增 5 张核心工单） |
| 代码实现 | **M0-01~M0-04 已落地**：`accounts` + `llm` + `gitlab_integration`（读：`/api/health/gitlab`；写演练：`POST /api/gitlab/smoke-write/` + `TC_GITLAB_ENABLE_WRITE`）；**W-A-04 全量自检**（PG / pre-commit）进行中 |
| Fork 起始 tag | 待 Platform Engineer 在 M0-01 启动时锁定并回写 PRD §2 |

---

## 角色概览

详见 PRD §4。一句话版本：

- **Owner**：工厂信息化负责人 / IT（不是开发者）
- **Reviewer**：业务使用者中参与 Preview 试用反馈的代表
- **Admin**：平台管理员 / 运维
- **Platform Engineer**：维护模板底座、Builder 运行时、LLM Gateway 的技术角色
- **Human Developer**：人工开发者（降级通道）
- **业务使用者 (End User)**：真正在车间 / 工位用系统的工厂人员；**不直接接触 Builder**

---

## 如何本地跑起来

### TimberClaw 业务骨架（M0-01 + M0-02）

在仓库根目录：

```bash
docker compose up --build
```

- **OpenHands**：`http://127.0.0.1:3000`（上游 UI）
- **工厂业务搭建（占位）**：`http://127.0.0.1:3000/tc`（Ant Design 业务壳，面向工厂 IT）
- **TimberClaw Django API**：`http://127.0.0.1:8000/api/health/`（健康检查）
- **PostgreSQL（Builder 元数据 / 业务库占位）**：宿主机端口默认 `5433`（可用环境变量 `TC_POSTGRES_PORT` 覆盖）

演示账号与后端测试（**仅内网 / 开发**）：

```bash
docker compose exec tc-backend python manage.py seed_builder_demo_users
docker compose run --rm tc-backend python -m pytest
```

Wave A 统一自检（**Postgres 宿主机端口** + **Django `/api/health/`**（经 `tc_compose_health.sh`）+ **LLM / GitLab**；需 `docker compose up` 后 Postgres 映射到 `127.0.0.1:${TC_POSTGRES_PORT:-5433}`、`tc-backend` 映射到 `8000`）：

```bash
bash scripts/tc_wave_a_check.sh
```

可选：在同一脚本内跑容器内 **pytest** 或本机 **pre-commit**（后者依赖 W-A-00 装好钩子）：

```bash
TC_WAVE_A_RUN_PYTEST=1 bash scripts/tc_wave_a_check.sh
TC_WAVE_A_RUN_PRE_COMMIT=1 bash scripts/tc_wave_a_check.sh
```

仅 Django 根健康：

```bash
bash scripts/tc_compose_health.sh
```

完整安装说明与自检（GitLab / LLM / pre-commit 全链路）仍以 **M0-05** 收口为准；上游 OpenHands 的本地开发流程见根目录 `README.md` 与 `AGENTS.md`。

---

## 贡献与协作

- 任何 Agent / 人工变更都必须通过 Git 分支 + PR，**合并到 `cursor`**，禁止直推 `cursor` 与 `main`
- 分支 / commit 命名见 [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) §4
- Agent 工作前必读 [`AGENTS.md`](AGENTS.md)

---

## 许可证

本仓库继承上游 OpenHands 的 **MIT 协议**。
