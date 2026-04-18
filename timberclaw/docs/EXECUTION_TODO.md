# TimberClaw 执行看板（实时 Todo）

> 目标：把"分阶段推进 + 实时状态更新 + 可并行拆分"落地为统一看板。
>
> 状态定义：`pending`（未开始）/ `in_progress`（进行中）/ `blocked`（阻塞）/ `done`（完成）

## 更新时间
- 2026-04-20 (UTC)（Wave A：`/api/health/` 增加数据库探测）

## 当前总览
- 当前波次：**Wave A（M0 基础设施）**；Wave B–G（M1–M8）仍见本文件后续章节与 `ROADMAP_EXECUTION_PLAN.md`，**未在单分支内「一次做完」**。
- 当前 Sprint：**Sprint-0（Wave A：M0-01~M0-04 推进中；合并目标分支 `cursor`）**
- **执行边界**：本看板列出 Wave A–G 全路线图；**不可能在单次迭代内全部实现**。交付按 Wave 顺序推进；`.github/workflows/timberclaw-builder.yml` 提供 TimberClaw 相关改动的 **可重复 CI 验收**（不等价于「所有工单已完成」）。
- 总计划：见 `timberclaw/docs/ROADMAP_EXECUTION_PLAN.md`
- 基线 PRD：V1.5；基线 BACKLOG：V1.2
- 下一里程碑出口：`docker compose up` 可拉起 Builder 基础能力（含 OpenHands 原屏 + `/tc/*` 占位 + PG）

## PRD V1.5 强约束（贯穿所有 Wave，不另开工单）

下列约束来自 PRD V1.5 + BACKLOG V1.2 顶部"既有工单需补充的新约束"，每个 Wave 验收前必须复核：

1. **概念隔离前置**（PRD §5.8）：从 Wave B 起，所有 Owner / Reviewer / 生成系统可见文案必须经过术语映射（详见 W-B-00）
2. **Spec 业务场景视图为默认**（PRD §8.2）：M1-01 / M1-02 输出的初始 spec 必须默认呈现业务场景视图
3. **模板底座一次性内置仪表盘 + 主数据导入**（PRD §8.3.1 / §8.12）：M2-01 必须为 M2-07 / M2-08 预留挂载点，避免回头返工
4. **`external_import` 实体生成约束**（PRD §8.12）：M2-05 不得为该类实体生成"新增 / 批量删除"按钮
5. **Dev 失败不直接抛 Owner**（PRD §8.6）：M3-01 失败路径必须接入 M3-05 通知分派
6. **数据治理前置**（PRD §10）：M7-01 / M7-03 / M7-04 与 Wave C/D 并行，而非堆到 Wave F

---

## Wave A · M0 基础设施

**Wave A DoD**（来自 ROADMAP §2）：
- `docker compose up` 可启动最小 Builder（OpenHands + Django + PG + 前端）
- 可访问 OpenHands 原屏与 `/tc/*` 占位页
- 可完成一次 GitLab 机器账号"分支→提交→MR"演练
- 自检脚本可输出 PG / GitLab / LLM 三项连通状态
- **pre-commit hooks 链路本地可用**（W-A-00 解锁）

### W-A-00: 修复 Poetry / pre-commit 环境（阻塞修复）
- 状态：`pending`（Makefile 已增加 `ensure-poetry-virtualenvs-path`；**本机** `make install-pre-commit-hooks` 仍待 Python 3.12 + Poetry 环境复验；仓库级 **pre-commit** 已由 `.github/workflows/lint.yml` 的 `lint-python` 以 pip 安装方式覆盖，与 Poetry 虚拟环境解耦）
- 依赖：无
- 关联 BACKLOG：M0-01 前置
- 范围：
  - 修复 `make install-pre-commit-hooks` 失败：`No such file or directory: /root/.cache/pypoetry/virtualenvs/envs.toml`
  - 重建 Poetry 虚拟环境目录与缓存
  - 验证 pre-commit 钩子在本地 commit 前可触发 lint / typecheck
- 验收：
  - `make install-pre-commit-hooks` 成功退出
  - 在测试 commit 中能看到 pre-commit 触发记录
  - 写入 `M0-05 自检脚本`：自检列表包含 pre-commit 链路通过

### W-A-01: M0-01 Builder 项目脚手架
- 状态：`done`（Batch 1–3 已完成；compose 全链路已由 Owner 确认）
- 依赖：W-A-00（pre-commit 缺失不影响代码落地，但影响 commit 前校验，建议并行修复）
- 关联 BACKLOG：M0-01
- 范围摘要：
  - 在 OpenHands fork 基础上叠加 TimberClaw 业务模块骨架
  - 打通 `/tc/*` 路由占位与基础布局入口
  - 扩展 compose 以纳入 Django + PostgreSQL（按最小侵入策略）
  - **预留**：在前端 `frontend/src/timberclaw/` 中预留 `dashboards/`、`master-data/` 目录（为 M2-07 / M2-08）
- 本次执行批次（Batch）
  - Batch 1：计划与任务切分（done）
  - Batch 2：仓库与目录落位初始化（done：`/tc/*` + Django + compose 骨架）
  - Batch 3：运行与连通性自检（done）

### W-A-02: M0-03 LLM Gateway 抽象
- 状态：`done`（MVP：`mock` / `openai` / `dashscope` 三出口；`/api/health/llm/`；`/api/llm/invoke/` + `LLMCallLog` + 出站脱敏工具 + Token 上限）
- 依赖：W-A-01
- 并行策略：与 W-A-03、W-A-05 并行
- 范围：抽象统一 LLM 出口；至少支持 OpenAI + 一家国内厂商；Token / 成功率 / 失败原因监控；单任务上限；出站脱敏
- 备注：调用统计当前以 **Django Admin → LLM 调用记录** 查看；后续可接 Wave G 指标看板

### W-A-03: M0-04 GitLab 接入
- 状态：`done`（阶段 A：`/api/health/gitlab/` + `TC_GITLAB_*`；阶段 B：`POST /api/gitlab/smoke-write/` 分支 / 提交 / MR，`TC_GITLAB_ENABLE_WRITE=1` + Platform Engineer）
- 依赖：W-A-01
- 并行策略：与 W-A-02、W-A-05 并行
- 范围：Project Access Token 配置；连通性自检；机器账号身份分支 / commit / MR

### W-A-04: M0-05 Builder 部署与自检
- 状态：`in_progress`（`tc_wave_a_check.sh`：PG 宿主机 TCP + `tc_compose_health.sh`（`/api/health/` 含 **DB**）+ LLM/GitLab；**可选** `TC_WAVE_A_RUN_PYTEST` / `TC_WAVE_A_RUN_PRE_COMMIT`；**CI**：`.github/workflows/timberclaw-builder.yml`（`main`/`cursor` + paths 过滤）跑 Docker **pytest**、compose 上 **tc_wave_a_check**、`frontend` 下 **`src/timberclaw` ESLint**；README「30 min deploy」叙事与是否默认跑 `TC_WAVE_A_RUN_PRE_COMMIT` 仍待 W-A-00 后收口）
- 依赖：W-A-00、W-A-01、W-A-02、W-A-03（均已满足；W-A-00 仍影响 pre-commit 是否默认可跑）
- 并行策略：Wave A 收口工单
- 范围：`docker-compose.yml` + README；启动自检脚本（PG 可达、GitLab 连通、LLM 连通）

### W-A-05: M0-02 认证与账号
- 状态：`done`（MVP：`UserProfile` 五角色 + Session/DRF 登录 + 示例门禁 + `seed_builder_demo_users` + `pytest`）
- 依赖：W-A-01
- 并行策略：与 W-A-02 / W-A-03 并行（本工单已可在 `tc-backend` 独立验收）
- 范围：Django 内置 auth + 五类角色（Owner / Reviewer / Admin / PE / Human Developer）+ 角色 × 动作权限
- 注意：业务使用者（End User，PRD §4.6）不在 Builder 账号体系内，仅在生成系统的运行时存在
- 验收命令（需 Docker）：`docker compose run --rm tc-backend python -m pytest`

---

## Wave B · M1 Spec 管道

**Wave B DoD**（来自 ROADMAP §2）：
- 同一份 spec 在"业务场景视图 + 结构化专业视图"可双向联动
- 未确认 spec 无法进入生成流程
- diff 可同时产出"业务摘要"和"结构化差异"
- **Owner UI 中无未经映射的工程术语**（W-B-00 拦截）

### W-B-00: 概念隔离最小子集前置（V1.5 关键修订）
- 状态：`pending`
- 依赖：W-A-01
- 并行策略：与 W-B-01 同步启动；属于 M4-06 的早交付子集
- 关联 BACKLOG：M4-06 最小子集（提前到 Wave B）
- 范围：
  - 全局术语映射层骨架（i18n 式键值表 + 角色上下文）
  - 覆盖 PRD §7.4 表的全部映射项（commit / PR / rc / Preview / Prod / migration / diff / 回滚）
  - 提供 ESLint / 文本扫描规则：检测 Owner / Reviewer / 生成系统目录中是否出现敏感词（`commit`、`rc-`、`PR `、`merge request`、`migration`、`diff` 等原文）
  - 接入 Dev 验证（M3-01 落地时只需挂上去即可）
- **不做**（留给 W-E-01 内的完整 M4-06）：
  - 候选版本相关的全部业务文案
  - Reviewer 严格映射（依赖 M4-03 Preview 落地）
- 验收：
  - 任一 Owner 业务屏（M1 范围内）打开后无原始工程英文词
  - ESLint 规则 CI 触发后能拦截违规提交

### W-B-01: M1-01 ~ M1-03（需求输入 + 初始 spec + 对话修订）
- 状态：`pending`
- 依赖：W-A-04（Wave A 收口）、W-A-05（认证）
- 关联 BACKLOG：M1-01 / M1-02 / M1-03
- 范围摘要：
  - M1-01 需求输入中心（上传 / 文本 / 对话 / 模板四种入口）
  - M1-02 Spec Analyst 生成初始 spec，**默认业务场景视图**（PRD V1.5 强约束 #2）
  - M1-03 自然语言对话修订 spec + 版本与 diff
- 子任务粒度：建议拆为 M1-01 / M1-02 / M1-03 三个独立条目（M1-02 依赖 M1-01；M1-03 依赖 M1-02）

### W-B-02: M1-04 + M1-06（结构化编辑 + 双视图）
- 状态：`pending`
- 依赖：M1-02 完成
- 并行策略：W-B-02 与 W-B-01 中 M1-03 可并行（均依赖 M1-02）
- 关联 BACKLOG：M1-04 / M1-06
- 范围摘要：
  - M1-04 结构化 spec 编辑器（ProTable / ProForm）
  - M1-06 双视图：业务场景视图 ↔ 结构化专业视图双向映射；diff 双份摘要
- 验收增量：Reviewer 账号无法进入任一 spec 视图

### W-B-03: M1-05 确认闸门
- 状态：`pending`
- 依赖：M1-03 + M1-04 + M1-06 全部完成
- 并行策略：Wave B 收口工单
- 关联 BACKLOG：M1-05
- 范围：spec 显式确认动作；未确认不进入 M2

---

## Wave C · M2 模板底座 + 首次代码生成

**Wave C DoD**（来自 ROADMAP §2）：
- 基于确认 spec 可生成"工单 + 报工 + 质检 + 仪表盘 + 主数据导入"的可运行项目
- Preview 能加载 fixtures
- `external_import` 实体页面满足"只读 + 导入 + 导出"约束
- **数据合同与写入边界已在生成代码中生效**（W-C-Aux 拦截）

### W-C-01: M2-01 ~ M2-03（前端 + 后端 + 部署模板底座）
- 状态：`pending`
- 依赖：W-A-04
- 并行策略：M2-01 / M2-02 可两路并行；M2-03 依赖二者
- 关联 BACKLOG：M2-01 / M2-02 / M2-03
- 范围摘要：
  - M2-01 React 18 + AntD v5 + ProTable / ProForm / ProLayout，**同时内置仪表盘页模板（M2-07）与主数据导入页模板（M2-08）的挂载点**（PRD V1.5 强约束 #3）
  - M2-02 Django + Auth/RBAC + CRUD + 状态机 + 操作日志 + Migration + pytest-django
  - M2-03 Preview / Prod 共用 docker-compose 模板 + 启停脚本

### W-C-02: M2-04 ~ M2-06（实现计划 + 首次生成 + fixtures）
- 状态：`pending`
- 依赖：W-B-03（M1-05 确认闸门）+ W-C-01
- 关联 BACKLOG：M2-04 / M2-05 / M2-06
- 范围摘要：
  - M2-04 App Architect：从 spec 产出实现计划
  - M2-05 Code Builder 首次生成；**对 `external_import` 实体不生成新增 / 批量删除按钮**（PRD V1.5 强约束 #4）
  - M2-06 fixtures 生成器（每核心对象至少 1 条覆盖每种主要状态）

### W-C-03: M2-07 + M2-08（仪表盘 + 主数据导入导出）
- 状态：`pending`
- 依赖：W-C-02 完成（M2-04 / M2-05 是生成链路前置）
- 关联 BACKLOG：M2-07 / M2-08
- 范围摘要：
  - M2-07 仪表盘一等公民：Ant Design Charts；4 类图表 + KPI + 明细 + 下钻；后端聚合接口；P95 ≤ 3s
  - M2-08 主数据导入：模板下载 + 预校验 + 业务键 upsert + 失败行下载 + 操作日志；列表 / 仪表盘 CSV 导出（UTF-8 + BOM）

### W-C-Aux: M7-01 + M7-03 + M7-04 数据治理前置（V1.5 修正）
- 状态：`pending`
- 依赖：W-C-01（需要 M2-02 后端模板）+ W-A-05（需要 M0-02 角色）
- 并行策略：与 W-C-02 / W-C-03 并行；属于 M7 子集前移（避免 Wave F 撞 M6 依赖）
- 关联 BACKLOG：M7-01 / M7-03 / M7-04
- 范围：
  - M7-01 数据合同注册表（核心对象主键 / 业务键 / 字段清单 / 状态枚举）
  - M7-03 写入边界（Prod 写入只走受控 API；状态机在服务层；权限到角色 × 动作）
  - M7-04 操作日志（who / when / what / target / source；source 枚举 `human_ui` / `agent_patch` / `migration_job` / `rollback`）
- 验收：
  - 缺失数据合同的对象在生成阶段被阻断（不必等到 M6-01）
  - 跳过服务层的写入尝试被拒绝
  - 关键动作 100% 落日志

---

## Wave D · M3 Dev 验证 + Git/PR

**Wave D DoD**（来自 ROADMAP §2）：
- Dev 验证链路可结构化出错并分派给 PE / Admin
- 低风险错误可自动修复（≤2 次）
- Owner 只接收人话摘要，不接原始工程噪音
- **术语扫描已挂入 Dev 验证**（W-B-00 产物落地）

### W-D-01: M3-01 ~ M3-03（验证编排 + 自动修复 + 风险识别）
- 状态：`pending`
- 依赖：W-C-02 完成
- 关联 BACKLOG：M3-01 / M3-02 / M3-03
- 范围摘要：
  - M3-01 串联 lint（ruff + eslint）/ typecheck（mypy + tsc）/ build / migration / pytest / vitest；**挂上 W-B-00 的术语扫描规则**
  - M3-02 Repair Agent 对确定性错误自动修复 ≤2 次
  - M3-03 高风险识别（migration / 认证授权 / 状态机 / 模板底座 / 新增一级依赖 / 连续 2 次修复失败）

### W-D-02: M3-04 分支与 MR 自动化
- 状态：`pending`
- 依赖：W-A-03（M0-04 GitLab）+ W-C-02（M2-05 代码生成）
- 并行策略：与 W-D-01 可并行（依赖完全独立）
- 关联 BACKLOG：M3-04
- 范围：分支命名 `tc/<spec_version>/<short_desc>`；自动 commit / 首次 MR；patch 持续更新同一 MR

### W-D-03: M3-05 Dev 失败通知分派
- 状态：`pending`
- 依赖：W-D-01 完成
- 关联 BACKLOG：M3-05
- 范围：
  - 失败分派：PE 首要 / Admin 次要 / Owner 仅在需改 spec 时被拉入决策
  - 通知双语化：PE 收原始工程术语；Owner 收 §7.4 映射后的人话
  - 通知渠道 MVP：站内消息 + 邮件
  - Owner 视图不显示未分派给自己的失败单细节

---

## Wave E · M4 候选版本 + Preview + M5 反馈闭环

**Wave E DoD**（来自 ROADMAP §2）：
- Owner 可创建版本 N（rc-N 映射）并触发在线试用
- Reviewer 可提交反馈，系统按低 / 高风险分流到 patch 或 spec 修订
- 术语映射扫描已接入 Dev 验证（在 W-D-01 已落）

### W-E-01: M4-01 ~ M4-05（候选版本 + Preview Runner）
- 状态：`pending`
- 依赖：W-D-02（M3-04 MR 自动化）+ W-C-01（M2-03 部署模板）
- 关联 BACKLOG：M4-01 / M4-02 / M4-03 / M4-04 / M4-05
- 范围摘要：
  - M4-01 ReleaseCandidate 数据模型（rc_number 按 PR 内部递增）
  - M4-02 Owner 创建 rc 的 UI（Dev 未通过禁用按钮）
  - M4-03 Preview Runner（Docker Compose；独立 PG 或 schema；URL + 状态 + 日志）
  - M4-04 Preview 生命周期（TTL 7 天 + 手动延长；rc 废弃即回收；失败重试 1 次）
  - M4-05 fixtures 加载

### W-E-02: M4-06 完整版语言映射层
- 状态：`pending`
- 依赖：W-B-00（最小子集）+ W-E-01（候选版本与 Preview 业务文案）
- 关联 BACKLOG：M4-06 完整范围
- 范围：
  - 候选版本 / Preview / 发布 / 反馈 / 通知 / 审计摘要全量走映射
  - Reviewer 严格映射（彻底屏蔽 rc 编号 → "版本 N"）
  - 生成系统采用最严映射（错误提示模板统一走底座）

### W-E-03: M5-01 ~ M5-05（反馈到 patch 闭环）
- 状态：`pending`
- 依赖：W-E-01 + W-D-01
- 关联 BACKLOG：M5-01 ~ M5-05
- 范围摘要：
  - M5-01 反馈面板（**所有文案走 M4-06 映射层**，PRD V1.5 强约束 #1 落地）
  - M5-02 反馈状态机（待处理 → 处理中 → 已 patch / 已拒绝 / 已关闭）
  - M5-03 风险判定（静态规则 + Agent 研判，Owner 可升降级）
  - M5-04 低风险自动 patch（更新 MR + 重跑 Dev）
  - M5-05 高风险强制走 spec → 代码

---

## Wave F · M6 Prod 发布 + 回滚 / M7 数据治理收尾

**Wave F DoD**（来自 ROADMAP §2，扣除已前移到 W-C-Aux 的部分）：
- Prod 发布具备人工确认与备注
- 回滚支持"上一个生效版本"一键回退
- 数据合同 / 写入边界 / 审计已在 Wave C 落地，本 Wave 收尾 migration 风险 / 备份 / Agent 数据权限

### W-F-01: M6-01 ~ M6-03（发布 + 回滚）
- 状态：`pending`
- 依赖：W-C-Aux（M7-04 操作日志）+ W-E-01（候选版本）
- 关联 BACKLOG：M6-01 / M6-02 / M6-03
- 范围摘要：
  - M6-01 Prod 发布页（汇总 rc / PR / spec / 验证 / 审计；备注必填）
  - M6-02 Prod Docker Compose 部署；Prod 数据库独立
  - M6-03 一步回滚到上一个 Prod 生效 rc；不可逆 migration 强制 PE 介入

### W-F-02: M7-02 + M7-05 + M7-06（数据治理收尾）
- 状态：`pending`
- 依赖：W-F-01 + W-C-Aux
- 关联 BACKLOG：M7-02 / M7-05 / M7-06
- 范围摘要：
  - M7-02 migration 高风险识别（删字段 / 改类型 / 改主键 / 拆合表 / 改状态枚举语义）
  - M7-05 操作日志保留 ≥180 天 + Prod 每日全量备份保留 ≥30 天 + 备份恢复演练
  - M7-06 Agent 数据权限分层（Dev / Preview / Prod）

---

## Wave G · M8 端到端冒烟 + 指标看板

**Wave G DoD**（来自 ROADMAP §2）：
- 离散制造首期五场景达到 PRD §13 指标基线
- 成功标准看板可手工复核
- PRD 对齐清单和 bug bash 结果可追踪

### W-G-00: §13 指标采集占位（前置）
- 状态：`pending`
- 依赖：W-D-01（Dev 验证）+ W-F-01（Prod 部署）+ W-C-Aux（操作日志）
- 并行策略：建议在 Wave E 末尾就开埋点占位，避免 Wave G 才发现没数据
- 范围：
  - 首次需求 → 首个 Preview 时长埋点（§13.1）
  - 反馈 → patch 时长埋点（§13.1）
  - Dev 一次性通过率 / Preview 部署成功率 / Prod 回滚时长（§13.4）
  - 概念隔离扫描违规计数（§13.2）

### W-G-01: M8-01 ~ M8-05
- 状态：`pending`
- 依赖：W-F-02 + W-G-00
- 关联 BACKLOG：M8-01 ~ M8-05
- 范围摘要：
  - M8-01 工单端到端：P50 ≤ 30 分钟
  - M8-02 报工闭环：反馈 → patch P50 ≤ 10 分钟；高风险强制走 spec
  - M8-03 质检发布与回滚：发布备注 + 回滚 ≤ 15 分钟
  - M8-04 成功标准看板（§13 四类指标）
  - M8-05 PRD 对齐 + bug bash → V1.6 候选修订

---

## 并行智能体编排

> W-A-02（LLM）MVP 与 W-A-03（含写路径 `smoke-write`）已落在 PR → `cursor`；W-A-04 自检脚本草案已起。

### Agent-Backend
- 负责：`timberclaw/backend/` Builder API、认证、LLM/GitLab 适配层
- 当前状态：`in_progress`（下一优先：W-A-04 全量自检与文档「30 min deploy」）
- 已完成：M0-01 骨架 + M0-02 `accounts` + M0-03 `llm` + M0-04 `gitlab_integration`（读 + `smoke-write` 写演练）

### Agent-Frontend
- 负责：`frontend/src/timberclaw/` 业务屏（Ant Design）
- 当前状态：`pending`（下一优先：对接 `/api/me` 展示当前登录角色；术语映射 W-B-00）
- 已完成：M0-01 `/tc/*` 占位与预留目录

### Agent-Infra
- 负责：compose、健康检查脚本、环境变量约定
- 当前状态：`in_progress`（下一优先：W-A-04 — PG / pre-commit 纳入统一自检）
- 已完成：M0-01 `postgres` + `tc-backend` + `tc_compose_health.sh` + `tc_wave_a_check.sh`（PG + API 链 + 可选 pytest/pre-commit）

### Agent-QA
- 负责：验收清单、命令验证、阻塞与风险归档
- 当前状态：`in_progress`
- 说明：维护执行看板；跟进 W-A-00 pre-commit 复验与 Wave A 收口证据链

---

## 风险与阻塞

1. **W-A-00 阻塞**：`make install-pre-commit-hooks` 失败（`No such file or directory: /root/.cache/pypoetry/virtualenvs/envs.toml`）
   - 影响：pre-commit 链路不可用 → 本地 commit 前无法触发 lint / typecheck → 与 Wave A DoD 中"自检脚本"承诺有缺口
   - 当前状态：已在 Makefile 增加 `ensure-poetry-virtualenvs-path`（创建并固定 `virtualenvs.path`）；待本机 / CI 复验后可将 W-A-00 标为 `done`
   - 修复策略：重建 Poetry 虚拟环境目录与缓存；纳入 M0-05 自检列表
   - 临时降级：M0-01 Batch 2 / Batch 3 期间，本地以"能跑的都跑"补偿（手工 lint / typecheck），不接受跳过 CI

2. ~~**Batch 3 环境**~~：已由 Owner 在本地 Docker 确认；CI 侧待 M0-05 接入统一自检

3. **依赖图风险**：M7-01 / M7-03 / M7-04 已前移到 W-C-Aux；若 Wave C 漏做，Wave F 的 M6-01 无法启动（M6-01 强依赖 M7-04 操作日志）

4. **Wave A 尚未整体 done**：M0-01 / M0-02 / M0-03 / M0-04（含写演练 API）已交付；**M0-05** 仍差「默认 CI / 文档承诺」级 pre-commit 与一键「30 min deploy」叙事收口；M1~M8 仍不得越级

---

## 下一步（Next Action）

1. **分支策略**：所有开发与 PR **以 `cursor` 为 base / 合并目标**（见 `docs/CONVENTIONS.md` §4.0）。
2. **合并 PR**：将 `tc/m0-wave-a/llm-gitlab-gateway` 合入 `cursor`（或继续在同分支迭代直至合并）。
3. **W-A-04 收口**：在 `tc_wave_a_check.sh` 已含 PG + 可选 pytest/pre-commit 基础上，补齐 **W-A-00 解锁后** 的默认 CI 步骤与 README「30 min deploy」清单。
4. **W-A-00**：`make install-pre-commit-hooks` 复验通过后标 `done`。
5. **Wave B 起跑**：W-B-00 术语映射 ESLint + W-B-01 需求输入中心。

---

## 更新规则

每次任务反馈时，必须更新以下字段：

1. 任务状态（pending / in_progress / blocked / done）
2. 当前批次（Batch）与完成结果
3. 风险与阻塞（新增 / 解除）
4. 下一步（Next Action）
5. **PRD V1.5 强约束区**：若新发现的强约束，需追加并标注影响的 Wave
