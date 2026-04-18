# TimberClaw-code

> 一个为**离散制造工厂**生成轻量 MES / BI 系统的 **Builder**。
>
> 让**工厂信息化负责人**从业务场景对话出发，先生成并确认 spec，再在受约束的模板底座内自动生成系统，在 Preview 中体验和反馈，在人工把关下发布到 Prod，最终由不懂代码的车间 / 排产 / 质检人员日常使用。

[![License](https://img.shields.io/badge/LICENSE-MIT-20B2AA?style=for-the-badge)](LICENSE)
[![Fork of](https://img.shields.io/badge/fork%20of-OpenHands-555?style=for-the-badge)](https://github.com/All-Hands-AI/OpenHands)
[![Status](https://img.shields.io/badge/status-bootstrap-orange?style=for-the-badge)](timberclaw/docs/BACKLOG.md)

---

## 这是什么

**TimberClaw-code** 是基于 [OpenHands](https://github.com/All-Hands-AI/OpenHands)（MIT）fork 改造的**工业业务系统 Builder**。它不是通用 AI 编程助手，而是针对一个具体问题的专用产品：

> 帮离散制造工厂（机加 / 装配 / 电子组装）快速搭建 **工单 + 报工 + 质检 + 基础仪表盘** 这类轻量 MES；之后还能按需扩展到采购、库存、质量、设备、看板等工业业务系统。

### 与上游 OpenHands 的关系

- 我们**保留**了 OpenHands 的 Agent 编排、代码改动工具、沙箱执行、React 前端栈
- 我们**新增**：工厂业务所需的 spec 管理、模板底座、候选版本与环境流转、仪表盘、主数据 CSV 导入、面向非技术用户的语言映射层
- 业务层代码**集中**在 `timberclaw/` 与 `frontend/src/timberclaw/` 下，**不散落**到上游目录
- 上游目录（`openhands/`、`frontend/src/` 其余部分）采用**最小侵入**策略；必要改动需登记在 [`timberclaw/docs/UPSTREAM_PATCHES.md`](timberclaw/docs/UPSTREAM_PATCHES.md)（首次改动时建）

---

## 第一次进入本仓库？按此顺序读

无论你是人还是 Coding Agent，**必须**按下表顺序阅读；每一层只在前一层的约束下生效：

| 顺序 | 文档 | 读者 | 内容 |
|------|------|------|------|
| 1 | **本 README** | 所有 | 仓库身份 + 导航 |
| 2 | [`timberclaw/AGENTS.md`](timberclaw/AGENTS.md) | Coding Agent / Human Developer | Coding Agent 工作指南（**动手前必读**） |
| 3 | [`timberclaw/docs/PRD.md`](timberclaw/docs/PRD.md) | 所有 | 产品**单一真相源**（V1.5） |
| 4 | [`timberclaw/docs/CONVENTIONS.md`](timberclaw/docs/CONVENTIONS.md) | 所有 | 仓库结构纪律 + 上游同步规则 + 分支 / commit 规范 |
| 5 | [`timberclaw/docs/BACKLOG.md`](timberclaw/docs/BACKLOG.md) | Coding Agent / Platform Engineer | 里程碑 M0–M8 + 50+ 张工单（含验收标准） |
| 6 | [`timberclaw/docs/FORK_CANDIDATES.md`](timberclaw/docs/FORK_CANDIDATES.md) | 参考 | 为什么选 OpenHands |

**优先级（冲突时按此判定）**：PRD → `timberclaw/AGENTS.md` → `timberclaw/docs/CONVENTIONS.md` → 根 [`AGENTS.md`](AGENTS.md)（上游 OpenHands 原文 + TimberClaw 前置提醒）→ 子目录 README。

---

## 当前状态

| 项 | 状态 |
|----|------|
| PRD | **V1.5**（面向离散制造 + 概念隔离 + 仪表盘一等公民 + CSV 主数据 + spec 双视图） |
| BACKLOG | **V1.2**（对齐 PRD V1.5；新增 5 张核心工单） |
| 代码实现 | **尚未开始**（bootstrap 阶段） |
| Fork 起始 tag | 待 Platform Engineer 在 BACKLOG M0-01 启动时锁定并回写 PRD §2 |

---

## 角色一览

详见 [PRD §4](timberclaw/docs/PRD.md)。一句话版本：

- **Owner** — 工厂信息化负责人 / IT（有技术素养但不是开发者）
- **Reviewer** — 业务使用者中参与 Preview 试用反馈的代表（班组长 / 排产主管 / 质检主管）
- **Admin** — 平台管理员 / 运维
- **Platform Engineer** — 维护模板底座、Builder 运行时、LLM Gateway 的技术角色
- **Human Developer** — 人工开发者（降级通道，走标准 Git + PR）
- **业务使用者 (End User)** — 车间 / 排产 / 质检 / 仓管等真正在生产中用系统的工厂人员；**不直接接触 Builder**

**概念隔离硬规则**：`commit` / `PR` / `rc-` / `migration` / `diff` / 堆栈 等工程词不得出现在 Owner / Reviewer / 生成系统的 UI 中；必须走 [PRD §7.4](timberclaw/docs/PRD.md) 的人话映射表。

---

## 本地运行

MVP 的本地启动还**没搭起来**——属于 BACKLOG **M0-01 + M0-05**。

在 M0 工单合入前，如果你想体验上游 OpenHands 本身的能力（了解 Agent 抽象），可按 OpenHands 原始流程：

```bash
export INSTALL_DOCKER=0
export RUNTIME=local
make build
make run FRONTEND_PORT=12000 FRONTEND_HOST=0.0.0.0 BACKEND_HOST=0.0.0.0
```

M0 完成后，TimberClaw 全栈启动将是一条命令：

```bash
docker compose up
```

届时本节会被回写，具体步骤以 M0-05 的产出为准。

---

## 怎么参与

- **所有**改动通过 Git 分支 + PR（Merge Request）进入 `main`；禁止直推
- Agent 分支：`tc/<spec_version>/<short_desc>`
- 人工分支：`dev/<github-handle>/<short_desc>`
- Commit 信息格式、`[tc-agent]` / `[upstream-patch]` 标记规则：见 [`CONVENTIONS.md`](timberclaw/docs/CONVENTIONS.md) §4
- Agent 动手前**必读** [`timberclaw/AGENTS.md`](timberclaw/AGENTS.md)
- Owner 不会在对话中口头覆盖 PRD；任何新需求都走 PRD 修订 PR

---

## 目录结构速览

```
TimberClaw/
├── README.md                     你在这里
├── AGENTS.md                     上游 OpenHands 开发指南（头部有 TimberClaw 前置提醒）
├── openhands/                    ← 上游：Agent 抽象、执行底座、工具集（最小侵入）
├── frontend/                     ← 上游：React + TS 前端
│   └── src/timberclaw/           （规划中）TimberClaw 新增业务屏（Ant Design v5）
├── timberclaw/                   ← TimberClaw 自己的代码与文档集中点
│   ├── README.md                   TimberClaw 侧入口
│   ├── AGENTS.md                   Coding Agent 工作指南（必读）
│   ├── docs/                       产品文档 / 工单清单 / 仓库约定 / 决策档案
│   ├── backend/                    （规划中）Django 业务后端
│   ├── templates/                  （规划中）生成系统的模板底座
│   ├── integrations/               （规划中）GitLab / LLM / 邮件通知适配
│   └── tooling/                    （规划中）compose 片段、脚本
├── docker-compose.yml            将在 M0-01 时扩展（[upstream-patch]）
├── LICENSE                       MIT（继承上游）
└── ... OpenHands 其他原目录与文件（CONTRIBUTING / COMMUNITY / Development.md 等）
```

---

## 许可证

本仓库继承上游 OpenHands 的 **[MIT 协议](LICENSE)**。`enterprise/` 目录沿用上游的独立许可条款（见 [`enterprise/LICENSE`](enterprise/LICENSE)）；TimberClaw 不使用也不发行 `enterprise/` 中的代码。

---

## 致谢上游

TimberClaw-code 建立在 [OpenHands](https://github.com/All-Hands-AI/OpenHands) 的肩膀上。OpenHands 开源的 Agent 编排能力、代码操作工具集、沙箱执行、完整的 React 前端架构，让 TimberClaw 能把全部精力放在**把"为工厂做业务系统"这件具体的事做对**上，而不是从零搭 Agent 框架。感谢 OpenHands 团队与贡献者。
