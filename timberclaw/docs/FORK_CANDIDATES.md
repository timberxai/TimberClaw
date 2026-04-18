# TimberClaw-code Fork 基座决策档案

**版本**：V1.2（状态：**已决策 — 采用 OpenHands**）
**用途**：记录在 TimberClaw-code 启动期，对若干开源 Coding Agent / Dev Agent 框架作为 fork 基座的评估结论。保留此文档为今后版本演进与备选方案参考。
**决策日期**：2026-04
**决策人**：Owner（Changhao）

---

## 1. 评估维度

| 维度 | 说明 |
|------|------|
| 技术栈匹配度 | 与 TimberClaw 目标栈（Python 后端 + React 前端 + PostgreSQL）的契合程度 |
| 协议可商用 | 是否 MIT / Apache-2.0 / BSD 等宽松许可 |
| 多 Agent 编排能力 | 是否原生支持多角色 / 多步骤 Agent 串联 |
| 代码改动粒度 | 是否能以"受约束生成"（非自由撰写任意文件）方式工作 |
| Git 集成 | 是否内置 PR / branch / commit 支持，能配合 TimberClaw 的 rc-N 流程 |
| 沙箱运行 | 是否提供隔离的代码执行环境 |
| 模板约束 | 是否允许我们叠加"固定模板底座 + 生成边界"而不被框架抢占 |
| 社区活跃度 | commit 频次、维护者数量、上游稳定性 |
| Fork 友好度 | 上游是否合并友好；我们长期维护 fork 的成本 |
| UI 可替换性 | 是否允许我们重写 / 共存自己的业务屏 |

---

## 2. 候选项对比（评估快照，不再追加新项）

### 2.1 OpenHands（<https://github.com/All-Hands-AI/OpenHands>）— **已采用**

- **栈**：Python 后端（FastAPI-like 执行层）+ React 前端 + Docker 沙箱；MIT
- **多 Agent 编排**：原生支持 Agent 多角色；自带事件流与动作空间抽象
- **代码改动粒度**：内置 `str_replace / create / run` 类工具；适合 TimberClaw 的模板约束改造
- **Git 集成**：内置 `git` 执行与 GitHub 操作；GitLab 需我们适配
- **沙箱**：Docker 沙箱成熟
- **UI**：开发者向（Agent 对话 / 代码 diff / 终端 / 文件树）；原屏沿用，不强行改写为 AntD，**在其上新增业务屏用 Ant Design v5**（见 PRD §6.1.1）
- **社区**：活跃，SWEBench 分数对标业界前列
- **改造成本**：**低到中**（保留前端栈、保留 Agent 抽象、仅叠加业务屏与 Django 业务后端 + LLM Gateway 配置化）

### 2.2 SWE-Agent

- **栈**：Python；无独立前端；命令行 / 研究项目风格
- **优势**：在 bug-fix / patch 生成能力上较强
- **劣势**：没有成熟 UI、没有 Preview / Prod 三环境概念、需完全自建前端
- **结论**：更像"库"而非"产品"，自建 UI 与 Git / 部署流的成本高于 OpenHands

### 2.3 Aider

- **栈**：Python CLI 工具
- **优势**：实际代码改动最小化做得不错
- **劣势**：定位为个人 CLI，无多 Agent 编排、无 UI、无环境流转
- **结论**：不适合做 Builder 产品基座

### 2.4 Devika

- **栈**：Python + Svelte 前端
- **劣势**：前端栈与 OpenHands / TimberClaw 目标不一致（Svelte vs React）；社区活跃度、维护稳定性明显弱于 OpenHands
- **结论**：不采用

### 2.5 Smol Developer / autodev 类

- **劣势**：概念验证项目，社区维护弱；缺失沙箱 / Git / Preview / Prod 所需的完整能力
- **结论**：不采用

---

## 3. 维度评分对比

评分：1 = 差，5 = 优。

| 维度 | OpenHands | SWE-Agent | Aider | Devika |
|------|-----------|-----------|-------|--------|
| 技术栈匹配度 | 5 | 4 | 3 | 2 |
| 协议可商用 | 5 (MIT) | 5 | 5 | 5 |
| 多 Agent 编排 | 5 | 3 | 1 | 3 |
| 代码改动粒度 | 5 | 4 | 4 | 3 |
| Git 集成 | 4 | 3 | 3 | 2 |
| 沙箱 | 5 | 3 | 2 | 3 |
| 模板约束 | 4 | 3 | 2 | 2 |
| 社区 | 5 | 4 | 4 | 2 |
| Fork 友好度 | 4 | 3 | 3 | 2 |
| UI 可替换性 | 3 (保留 React，新业务屏 AntD 叠加) | 2 (无 UI) | 1 (无 UI) | 3 |
| **合计** | **45** | **34** | **28** | **27** |

---

## 4. 决策结论

**已采用：OpenHands + 保留 React 栈 + 引入 Ant Design v5 + TimberClaw 自研产品层**

理由：

1. OpenHands 在多 Agent 编排、沙箱、代码改动粒度上已经做得最完整，是能直接支撑 TimberClaw §8.5 Agent Orchestrator 的最短路径
2. 保留 OpenHands 前端栈（React 18 + TypeScript + Vite）避免了大量 UI 重写工作，上游同步成本最低
3. TimberClaw 新增的业务屏（需求输入、spec、候选版本、Preview、发布、反馈、审计）以 Ant Design v5 实现，通过路由前缀 `/tc/*` 与布局壳与 OpenHands 原屏共存，不强改原 UI
4. 生成系统（Builder 的输出物）统一采用 React 18 + TypeScript + Ant Design v5（与业务屏一致，便于模板复用）

**改造切入点**（已进入 BACKLOG M0-M8）：

- `openhands/` 原目录不改写，仅扩展
- 新增 `timberclaw/` 业务后端目录（Django 业务服务、LLM Gateway 配置化、GitLab 适配、rc-N 生命周期）
- 前端在 `frontend/src/timberclaw/` 下新增 AntD 业务屏
- 模板底座作为独立可生成工程（不是 OpenHands 子模块）
- LLM Gateway 从 OpenHands 原 LLM 调用抽象上再抽一层，支持配置切换与出站审计 / 敏感字段脱敏

---

## 5. 下一步行动（进入 BACKLOG 跟踪）

1. 锁定 fork 起始 commit / release tag（Platform Engineer 在 M0-01 启动时以增量修订方式补入 PRD §2）
2. 按 BACKLOG M0-01 搭建"OpenHands fork + TimberClaw 业务模块"并发生成的 docker-compose
3. 对上游做**最小侵入**修改，所有 TimberClaw 新增代码尽量落在独立目录（见 `CONVENTIONS.md`）
4. 后续如需评估其他 Agent 框架（例如新兴项目），不再改动本文件；改在 PRD 或新备选档案里追加
