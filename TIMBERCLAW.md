# TimberClaw-code

> 本仓库是 [OpenHands](https://github.com/All-Hands-AI/OpenHands) 的 **fork**。它不再是一个通用的 AI 软件工程师工具，而是被改造为 **TimberClaw-code**——一个为离散制造工厂生成轻量 MES / BI 系统的 Builder。

## 如果你是人 / AI Agent，第一次进入本仓库

**请按此顺序阅读**：

1. [`timberclaw/README.md`](timberclaw/README.md) — 项目入口
2. [`timberclaw/AGENTS.md`](timberclaw/AGENTS.md) — Coding Agent 工作指南（**必读**）
3. [`timberclaw/docs/PRD.md`](timberclaw/docs/PRD.md) — 产品单一真相源
4. [`timberclaw/docs/CONVENTIONS.md`](timberclaw/docs/CONVENTIONS.md) — 仓库结构纪律 + 上游同步规则
5. [`timberclaw/docs/BACKLOG.md`](timberclaw/docs/BACKLOG.md) — 工单清单（M0–M8）
6. [`timberclaw/docs/FORK_CANDIDATES.md`](timberclaw/docs/FORK_CANDIDATES.md) — 为什么选 OpenHands

## OpenHands 原始文档

仓库根目录下 [`README.md`](README.md) 和 [`AGENTS.md`](AGENTS.md) 是**上游 OpenHands 自带**的文档，描述的是 OpenHands 项目的安装 / 启动 / 使用方法。这些信息在开发环境与工具链层面仍然适用，但当你做**业务性或产品性决策**时，**始终以 TimberClaw 侧文档（上表）为准**。

## 核心纪律（必读摘要）

- **默认分支 `main` 受保护**，禁止直推
- TimberClaw 自己写的代码集中落位：`timberclaw/`（后端 / 文档 / 模板 / Agent 扩展）与 `frontend/src/timberclaw/`（AntD 业务屏）
- 修改上游目录必须用 `[upstream-patch]` 标记并登记到 `timberclaw/docs/UPSTREAM_PATCHES.md`
- 用户可见 UI 中**不得**出现 `commit` / `PR` / `rc-` / `migration` 等工程词；必须走 §7.4 的人话映射

## 许可证

继承上游 OpenHands 的 **MIT** 协议。
