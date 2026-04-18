# TimberClaw-code 仓库约定（Monorepo Conventions）

**版本**：V1.0
**用途**：本文件定义 TimberClaw-code（OpenHands fork）作为 monorepo 的结构纪律、代码落位、上游同步、分支与提交规范。**所有 Coding Agent 与 Human Developer 必须遵守。**

本文件的优先级：PRD > AGENTS.md > CONVENTIONS.md（本文件）> 仓库各子目录的 README。

---

## 1. 仓库身份

- 本仓库是 **OpenHands** 的 fork，但项目目标是 **TimberClaw-code**（详见 `docs/PRD.md` 第 2 节）
- 上游：<https://github.com/All-Hands-AI/OpenHands>（MIT）
- 默认分支：`main`（受保护，禁止直接推）
- 所有 TimberClaw 自身代码与文档都在 `timberclaw/` 子目录或约定的子路径下（见下方 §3）

---

## 2. 三条核心纪律

### 纪律 A：上游最小侵入

- **尽量不修改 OpenHands 原文件**。有改动需求时：
  - **优先**：在 `timberclaw/` 下新增模块 / 扩展 / 适配器
  - **其次**：通过配置注入或依赖注入改变行为
  - **最后**（确实必须改上游文件）：改动必须用 `# timberclaw:patch` 或 `// timberclaw:patch` 注释块包裹起止，并在 commit 信息里标记 `[upstream-patch]`，同时在 `timberclaw/docs/UPSTREAM_PATCHES.md`（首次改动时新建）登记
- 上游路径清单（未经登记**不得**修改）：`openhands/`、`frontend/src/`（除 `frontend/src/timberclaw/` 子目录）、`pyproject.toml`、`Makefile`、根目录 `AGENTS.md`、`README.md`、`config.template.toml`、`docker-compose.yml`、`tests/`、`third_party/`、`enterprise/`、`docs/`、`openhands-ui/`
  - 有些改动（例如在根 `docker-compose.yml` 引入 Django 服务）短期内是必须的；按上述 `[upstream-patch]` 流程处理

### 纪律 B：TimberClaw 代码集中落位

所有 TimberClaw 自己写的代码 / 文档 / 配置，集中落位在以下路径之一：

```
timberclaw/                 ← 业务后端 + 文档 + Agent 扩展 + LLM Gateway
frontend/src/timberclaw/    ← 业务前端屏（Ant Design v5）
```

禁止把 TimberClaw 的业务代码散落到 `openhands/`、`frontend/src/pages`、`frontend/src/components` 等上游目录下。

### 纪律 C：生成系统不等于 Builder 自身

TimberClaw 的"输出物"（Code Builder 生成的系统）**不落在本仓库**；每个生成系统作为独立 Git 仓库存在（由 Builder 在 GitLab 上自动创建）。本仓库只包含：

- Builder 本体（OpenHands + `timberclaw/` 扩展）
- **模板底座源代码**（作为本仓库中的一个子项目，Builder 从中复制并参数化以生成新系统）

模板底座落位：`timberclaw/templates/baseline/`（尚未搭建，见 BACKLOG M2-01 / M2-02）。

---

## 3. 目录约定

### 3.1 上游目录（最小侵入）

| 路径 | 用途 | TimberClaw 是否允许改 |
|------|------|----------------------|
| `openhands/` | OpenHands 核心（Python） | 禁止直接改；必要时走 `[upstream-patch]` 并登记 |
| `frontend/src/` | OpenHands 前端（React + TS） | 除 `frontend/src/timberclaw/` 外禁止直接改 |
| `docker-compose.yml` | 统一 compose（需引入 Django 业务后端） | 允许扩展，commit 标记 `[upstream-patch]` |
| `pyproject.toml` | Python 依赖 | 允许追加依赖段落，不得删减原依赖 |
| 其他上游目录 | 构建 / CI / 文档等 | 禁止改，除非登记 |

### 3.2 TimberClaw 专属目录（随意扩展）

```
timberclaw/
├── README.md                       TimberClaw 侧入口（已有）
├── AGENTS.md                       Coding Agent 工作指南（已有）
├── docs/                           所有 TimberClaw 产品 / 设计 / 决策文档
│   ├── PRD.md                      V1.5 单一真相源
│   ├── BACKLOG.md                  V1.2 工单清单
│   ├── FORK_CANDIDATES.md          fork 基座决策档案
│   ├── CONVENTIONS.md              本文件
│   └── UPSTREAM_PATCHES.md         上游修改登记册（首次需要时新建）
├── backend/                        Django 业务后端（尚未搭建，BACKLOG M0-01）
│   ├── manage.py
│   ├── tc_core/                    项目配置、路由、LLM Gateway、GitLab 适配
│   ├── tc_spec/                    Spec 管理（M1）
│   ├── tc_build/                   Code Builder / App Architect（M2）
│   ├── tc_release/                 候选版本 / Preview / Prod 发布（M4-M6）
│   ├── tc_feedback/                反馈采集与 patch 闭环（M5）
│   ├── tc_data/                    主数据导入 / 导出 / 审计（M7、M2-08）
│   └── tc_agents/                  Agent 编排层（基于 OpenHands Agent 抽象之上）
├── templates/                      生成系统的模板底座源代码
│   └── baseline/                   唯一模板（React + TS + AntD + Django + PG，BACKLOG M2）
├── integrations/                   外部集成（GitLab MR / LLM 云厂商 / 邮件通知）
└── tooling/                        脚本、Docker 片段、开发工具
    ├── compose/                    TimberClaw 自有的 compose 片段（被根 compose include）
    └── scripts/                    部署自检、备份脚本（M0-05、§9.5）

frontend/src/timberclaw/            TimberClaw 新增业务屏（AntD v5）
├── layouts/                        ProLayout 壳 + 面向业务用户的语言映射层（M4-06）
├── pages/                          业务屏：需求输入 / spec 双视图 / 候选版本 / Preview / 发布 / 反馈
├── components/                     业务屏共用组件（术语映射、仪表盘壳、主数据导入页等）
└── routes.tsx                      `/tc/*` 路由挂载
```

> 尚未搭建的目录由 BACKLOG M0-01 统一创建；Agent 在首次落位时必须严格按本结构，不得即兴发明子目录。

---

## 4. 分支与提交

### 4.1 分支命名

| 用途 | 格式 | 示例 |
|------|------|------|
| Agent 生成分支 | `tc/<spec_version>/<short_desc>` | `tc/v0.3.1/workorder-crud` |
| 人工开发分支 | `dev/<github-handle>/<short_desc>` | `dev/changhao/fix-import-csv` |
| 文档 / bootstrap / 基础设施 | `docs/<short_desc>` 或 `chore/<short_desc>` | `docs/v1.5-bootstrap` |
| 上游同步 | `upstream/sync-<yyyymmdd>` | `upstream/sync-20260420` |

禁止：直接向 `main` 推送；跨工单合并一个分支；branch 名里出现中文。

### 4.2 Commit 信息

格式：`<type>(<scope>): <summary>` + `[upstream-patch]` / `[tc-agent]` 等标记

- `type` 取值：`feat`、`fix`、`docs`、`refactor`、`chore`、`test`、`perf`
- `scope` 例子：`spec`、`builder`、`preview`、`release`、`feedback`、`data`、`frontend`
- `[tc-agent]` 标记：Agent 生成的 commit 必须带此标记，便于审计过滤
- `[upstream-patch]` 标记：改动了上游目录的 commit 必须带此标记，且 commit 信息里说明"为什么不能落在 timberclaw/ 下"

示例：

```
feat(spec): 引入 spec 双视图 [tc-agent]

- 业务场景视图卡片组件（frontend/src/timberclaw/pages/spec/scenarios）
- 结构化专业视图扩展现有 ProTable
- 双视图共享 tc_spec.models.SpecVersion（未改底层模型）

refs: BACKLOG M1-06, PRD §8.2
```

### 4.3 PR（MR）描述必填

- 关联 BACKLOG 工单 ID
- 关联 PRD 章节号
- 本次改动覆盖的验收标准勾选状态
- 是否触及上游目录；若是，列出 `[upstream-patch]` 范围

---

## 5. 上游同步策略

TimberClaw fork 与 OpenHands 上游的同步**手动触发**，节奏：每季度或上游有重要安全 / 能力更新时。

流程：

1. Platform Engineer 从上游 `main` 拉取最新 commit；在本仓库开 `upstream/sync-<yyyymmdd>` 分支
2. 合并冲突必须逐点评估：
   - 冲突在 `openhands/` / `frontend/src/`：**优先保留上游**；我们的 `[upstream-patch]` 如不再必要则删除
   - 冲突在 `timberclaw/` / `frontend/src/timberclaw/`：**保留我们的**
   - 冲突在 `docker-compose.yml` / `pyproject.toml`：人工逐段取舍
3. 合并完成后必须跑一轮完整 Dev 验证 + 端到端冒烟（BACKLOG M8）
4. 通过后以 MR 合回 `main`；MR 必须 Owner 签字

禁止：在 Agent 生成流中自动合并上游；Agent 不具备判断上游变更对 TimberClaw 影响的能力。

---

## 6. 语言与术语

TimberClaw-code 的代码内部不避讳使用英文工程术语，但**用户可见的任何文案**必须走 `frontend/src/timberclaw/layouts/i18n`（BACKLOG M4-06）做映射，详见 PRD §5.8 与 §7.4。

代码注释语言：中英文皆可，但同一文件内应保持一致。

---

## 7. 何时回改本文件

本文件本身不是"一次写死"。当以下情况发生时，允许通过 PR 修订：

- 新增子目录（例如未来加 `timberclaw/ml/` 做自建模型）
- 上游 OpenHands 发生重大目录结构变化
- 新增一类不适合任何现有 scope 的 commit type / 标记

修订必须在 PR 描述中说明理由，Owner 签字后合入。
