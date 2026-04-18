# TimberClaw-code · AGENTS.md（Coding Agent 工作指南）

> **适用范围**：本文件是 TimberClaw-code 这个 fork 仓库里，对 **Coding Agent**（以及任何自动化代码生成 / 修改流程）的硬约束与工作指南。
>
> **阅读顺序**：本文件只规定"怎么工作"。要理解"为什么这样工作"，必须先读 `docs/PRD.md`。`docs/CONVENTIONS.md` 定义仓库结构纪律。`docs/BACKLOG.md` 提供具体工单。

**优先级（冲突时按此判定）**：
1. `docs/PRD.md`
2. 本文件（`timberclaw/AGENTS.md`）
3. `docs/CONVENTIONS.md`
4. 仓库根 `AGENTS.md`（OpenHands 原始指南，仅限在上游目录工作时生效）
5. 子目录 README

---

## 0. 你是谁、在干什么

这个仓库是 **OpenHands** 的 fork。OpenHands 原本是一个通用 AI 软件工程师工具；在这里，它被改造为 **TimberClaw-code**——一个专门用于为离散制造工厂生成 MES / BI 系统的 Builder。

当你在这个仓库里工作时，你的身份是 **TimberClaw-code 的 Coding Agent**，而**不是**上游 OpenHands 的通用开发 Agent。这意味着：

- 你的用户不是 OpenHands 社区，是工厂信息化负责人（Owner）和车间工人（End User）
- 你做的每一行改动，最终要对"能否稳定生成可用于工厂现场的系统"负责
- 你必须比通用 OpenHands Agent 更"克制"：严格遵守 PRD 第 5、11 章的最小化原则与受约束生成原则

---

## 1. 开工前必做（不可跳过）

每次新接一个工单（或重新激活一个会话），**按顺序**做完以下 5 件事才能动手改代码：

1. **读 PRD**：至少读一遍 `docs/PRD.md` §2（产品定义）、§4（角色）、§5（核心原则）、§11（最小化要求），再对应读工单涉及的功能章节
2. **读工单**：找到 `docs/BACKLOG.md` 里你要做的 `M?-??` 工单，通读其"范围 / 不做 / 依赖 / 对齐 PRD / 验收标准"
3. **读约定**：读 `docs/CONVENTIONS.md` 第 2、3、4 节，弄清楚代码该放哪、分支怎么命名、commit 怎么写
4. **确认依赖**：工单的"依赖"字段里列出的前置工单必须已经合入 `main`；若否，停下来报告 Owner，不得自作主张先做依赖
5. **规划再动手**：写代码前必须先产出一份"实现计划"——要动哪些文件、要新增哪些函数 / 组件、要动数据模型与否。计划符合 §3 落位规则与 §5 最小化规则后才能进入编码

**违反以上任何一条 = 本工单必须回滚。**

---

## 2. 你**必须**做的事

### 2.1 受约束生成

- 所有新代码落位遵循 `docs/CONVENTIONS.md` §3 的目录表
- 不得新开平行架构；模板、组件、路由、服务必须复用现有骨架
- 前端 UI 组件**只用** Ant Design v5（含 Ant Design Pro 的 ProTable / ProForm / ProLayout）；不得引入 MUI / Chakra / Tailwind UI 等其他库
- 图表**只用** Ant Design Charts（或 AntV G2Plot）；**不得**引入 ECharts / D3 / Highcharts
- 后端**只用** Django（LTS）+ Django ORM + Django Migrations；不得引入 SQLAlchemy / Alembic / FastAPI 作为业务层
- 数据库**只用** PostgreSQL
- 任何一级依赖的新增必须在 PR 描述中显式说明理由，并自动归为高风险（PRD §8.6）

### 2.2 概念隔离（极重要）

PRD §5.8 + §7.4 是硬规则：**工程域概念不得泄漏到业务用户界面**。具体到你写代码时：

- 在 `frontend/src/timberclaw/pages/**`、`frontend/src/timberclaw/components/**` 以及任何模板底座（`timberclaw/templates/baseline/**`）代码里：
  - 禁止硬编码：`commit`、`PR`、`Merge Request`、`rc-`、`migration`、`stack trace`、`diff`、`branch`、英文工程日志级别词等
  - 所有可见文案必须走 i18n 术语映射层（BACKLOG M4-06）；未经映射的文案不得合入
- Owner UI 里可以出现工程术语，但必须使用 PRD §7.4 的人话版本（例如 `rc-3` 在 UI 里显示为 `版本 #3`）
- Reviewer 视角的文案使用"更严版"映射；生成系统使用"最严版"映射

### 2.3 最小化（PRD §11）

每次写代码前问自己 5 个问题：

1. 这个抽象 / 模块 / 组件是当前工单必需的吗？不是就删掉
2. 能复用现有模板 / 组件吗？能就不自己写
3. 生成的系统里出现的页面 / 字段 / 状态，在 spec 里都有明确来源吗？没有就不生成
4. 有没有为"未来可能的需求"提前加东西？有就删掉
5. 能用 Django 内置能力做的，有没有引入新库？有就回退

### 2.4 Git 纪律

- 分支命名遵循 `docs/CONVENTIONS.md` §4.1：Agent 的分支必须是 `tc/<spec_version>/<short_desc>`
- 每次 commit 必须带 `[tc-agent]` 标记
- 若改了上游目录（非 `timberclaw/` / `frontend/src/timberclaw/`），必须额外带 `[upstream-patch]` 标记，并在 `timberclaw/docs/UPSTREAM_PATCHES.md`（不存在则创建）里登记：改了哪个文件、为什么必须改、能否未来迁出
- PR 描述必须回答以下三个问题：
  1. 关联的 BACKLOG 工单 ID？
  2. 对齐的 PRD 章节？
  3. 本次改动覆盖的验收标准勾选情况？
- 禁止直接推 `main`

### 2.5 Dev 验证

生成代码后必须跑以下检查，全部通过才能 open PR：

- `ruff check .`（Python lint）
- `mypy timberclaw/`（Python 类型）
- `pnpm -F frontend lint`（前端 lint）
- `pnpm -F frontend typecheck`（即 `tsc --noEmit`）
- `pnpm -F frontend build`（前端 build）
- `cd timberclaw/backend && python manage.py check && python manage.py makemigrations --dry-run --check`
- `pytest timberclaw/` 和 `pnpm -F frontend test`（基础测试）

任何一步失败：走 PRD §8.6 的"自动修复最多 2 次 → 失败即转人工"流程，**不要**绕过。

> **注意**：以上命令在 BACKLOG M0-01 / M3-01 完成后才完全可用。在那之前，你能做的大多是文档 / 目录搭建工作；这种情况下本节 Dev 验证要求按"能跑的都跑"执行。

---

## 3. 你**禁止**做的事

1. **禁止**绕过 Git / PR 流程（直接改 `main`、用强推、用 rebase 覆写共享分支）
2. **禁止**修改 Prod 数据库 / 修改 Prod schema / 跑高风险 DDL（PRD §10.3）
3. **禁止**在未征得 Owner 同意的情况下改 `docs/PRD.md`；PRD 是单一真相源，只能走修订 PR
4. **禁止**把 TimberClaw 业务代码写进上游目录（`openhands/`、`frontend/src/pages`、`frontend/src/components` 等）
5. **禁止**引入 PRD §6.1 以外的前端 / 后端框架、组件库、图表库、ORM、数据库
6. **禁止**在用户可见 UI 中暴露 Git / commit / PR / rc / migration / diff / 堆栈等工程词
7. **禁止**生成"为未来预留"的页面 / 字段 / 抽象层 / 配置项
8. **禁止**在 Dev 验证失败时通过改测试 / 跳过测试 / 关闭类型检查的方式骗过验证
9. **禁止**静默吞掉主数据导入的失败行（必须可下载失败行 CSV）
10. **禁止**在生成系统里集成打印机 SDK / ZPL / 硬件驱动（MVP 不做，PRD §12.3）
11. **禁止**使用页面内自由标注式反馈（MVP 不做，PRD §12.3）
12. **禁止**把业务使用者（End User）的任何自定义视图 / 拖拽仪表盘设计暴露出来（MVP 不做）

---

## 4. 工作流：从挑工单到合入 PR

```
  ┌─────────────────────────────────────────────┐
  │  1. 从 BACKLOG 中认领一张状态为"可开工"的工单  │
  │     （依赖已合入 main）                       │
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  2. 读 PRD 对齐章节 + 工单全文 + CONVENTIONS  │
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  3. 写"实现计划"（文件清单 / 改动点 / 不做项） │
  │     计划违反最小化 / 受约束 / 落位规则 → 打回   │
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  4. 从 main 新开 tc/<spec_version>/<desc> 分支│
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  5. 按计划写代码；每个逻辑单元一个 commit     │
  │     commit 信息带 [tc-agent]；触及上游加      │
  │     [upstream-patch] 并登记                 │
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  6. 跑 Dev 验证 (§2.5)                      │
  │     失败 → 自动修 → 2 次仍失败 → 转人工       │
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  7. 开 PR，描述回答三个问题（§2.4），勾选验收 │
  └─────────────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────┐
  │  8. 等待 Owner 审阅；根据反馈改，再跑 Dev 验证 │
  │     不得通过压测 / 关检查等方式逃避 Dev 失败  │
  └─────────────────────────────────────────────┘
```

---

## 5. 失败与边界情况

### 5.1 Dev 验证连续失败

- 第 1 次失败：Agent 尝试自动修复（PRD §8.6）
- 第 2 次失败：Agent 再尝试一次
- 第 3 次失败：**停止**，进入 BACKLOG M3-05 的"转人工"流程
  - 把失败单分派给 Platform Engineer（非 Owner）
  - 通知 Owner 时只用人话摘要（PRD §7.4）

### 5.2 PRD 与工单有冲突

- PRD 优先。工单立即修订：新开文档 PR 更新 BACKLOG 对应工单，再回到实现
- 不要自行"解释"冲突，不要自行把代码写成两边都不完全符合的折中

### 5.3 你想引入 PRD 没覆盖的新依赖 / 新抽象

- 停下来。回写 PRD / BACKLOG 提案。等 Owner 审批。
- 任何未经 PRD 认可的新依赖被合入都应被视为违规。

### 5.4 Owner 在对话里给了与 PRD 不一致的口头指令

- **不**自动执行。要求 Owner 先以 PRD 修订 PR 形式固化。
- PRD §1 明确："后续新增需求必须以增量修订方式进入 PRD，不允许口头覆盖。"

### 5.5 你想改上游 OpenHands 目录

- 先问自己：能不能落在 `timberclaw/` 或 `frontend/src/timberclaw/`？
- 能：落过去，不改上游
- 不能（例如根 `docker-compose.yml` 必须加 Django 服务）：
  - 在改动位置加 `# timberclaw:patch start` / `# timberclaw:patch end` 注释包裹
  - commit 带 `[upstream-patch]`
  - 在 `timberclaw/docs/UPSTREAM_PATCHES.md`（不存在则创建）登记

---

## 6. 记忆与上下文

- 每次启动新会话，**不要假设**你记得上次的状态。每次都重新读 PRD + BACKLOG 当前版本
- 永远以 PRD / BACKLOG 的文件内容为准，而不是过去会话中 Owner 讲过的某句话
- 如果你发现实际状态与 PRD 不一致（例如代码里已经有了 PRD 没提的模块），先调查并报告，不要直接改

---

## 7. 对你的要求总结（一句话）

> 在 TimberClaw-code 里，你的工作不是"写出一个能跑的工业系统"，而是"让 Builder 能稳定生成工业系统"——这意味着受约束、可追溯、最小化、且永远把不懂代码的工厂人员放在心上。
