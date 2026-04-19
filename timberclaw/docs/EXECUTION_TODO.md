# TimberClaw 执行看板（实时 Todo）

> 目标：把"分阶段推进 + 实时状态更新 + 可并行拆分"落地为统一看板。
>
> 状态定义：`pending`（未开始）/ `in_progress`（进行中）/ `blocked`（阻塞）/ `done`（完成）
>
> **本文件是 Coding Agent 唯一调度面**（PRD §15.1）。Agent 按 §15.3 Pickup 协议挑工单；不得绕过本文件。

## 更新时间
- 2026-04-20 (UTC)（**W-B-00** → `done`：§7.4 全键 + `ddl_change` 命名约定 + timberclaw ESLint 扩展 + `npm run typecheck`）

## 当前总览
- 当前波次：**Wave A** 仅剩 **W-A-00**；**Wave B** **W-B-00 `done`** → **下一 Pickup：W-B-01**（可与 W-A-00 并行，由不同 Agent 承担）。
- 当前 Sprint：**Sprint-0 / Sprint-1 交界（合并目标分支 `cursor`）**
- **执行边界**：本看板列出 Wave A–G 全路线图；**不可能在单次迭代内全部实现**。`.github/workflows/timberclaw-builder.yml` 提供 TimberClaw 相关改动的 **可重复 CI 验收**（不等价于「所有工单已完成」）。
- 总计划：见 `timberclaw/docs/ROADMAP_EXECUTION_PLAN.md`
- 基线 PRD：**V1.6**；基线 BACKLOG：V1.2
- 下一里程碑出口（Wave A 完整 DoD）：`docker compose up` 可拉起 OpenHands 原屏 + `/tc/*` 占位 + PG + LLM/GitLab 自检；Wave A CI 全绿

---

## Coding Agent 续作协议（速查；正式定义见 PRD §15）

1. **Pickup 顺序**：当前 Wave 内 `in_progress` 且未阻塞 → 当前 Wave 内 `pending` 且依赖全 `done` → 下一 Wave 中依赖全 `done` 的 `pending`；都没有就 **停止并报告**（PRD §15.6）。
2. **认领**：把状态改成 `in_progress`，commit 带 `[tc-agent]`；同一时间一张工单只允许一个 Agent 在改。
3. **执行边界**：只动工单 `Range` 列出的代码 / 文档面；越权请新开工单，**不**改写当前 Range。
4. **收口**：满足 `DoD` 后状态改 `done`，把 `Evidence` 命令的输出粘到 PR 描述，PR base 必须是 `cursor`。
5. **停止信号**：见 PRD §15.6（无可 Pickup / 依赖被破坏 / CI 连续失败 / PRD 与 TODO 冲突 / 范围不足 / 触碰高风险）。

### 工单模板（新增工单时复制此块）

```
### W-?-??: <标题>
- 状态：pending
- 依赖：<工单 ID 列表，或 无>
- 关联 BACKLOG：<M-编号>
- 范围（Range）：
  - <允许动到的目录 / 文件 / 模块>
- Pickup 信号：
  - <可机读的就绪条件>
- DoD：
  - <验收条目 1（命令 + 期望输出）>
  - <验收条目 2>
- Evidence（PR 必跑命令）：
  - <命令 1>
  - <命令 2>
- 不做：
  - <明示越权项>
```

## PRD V1.6 强约束（贯穿所有 Wave，不另开工单）

下列约束来自 PRD V1.5 业务面 + V1.6 工作模式面 + BACKLOG V1.2 顶部"既有工单需补充的新约束"，每个 Wave 验收前必须复核：

1. **概念隔离前置**（PRD §5.8）：从 Wave B 起，所有 Owner / Reviewer / 生成系统可见文案必须经过术语映射（详见 W-B-00）
2. **Spec 业务场景视图为默认**（PRD §8.2）：M1-01 / M1-02 输出的初始 spec 必须默认呈现业务场景视图
3. **模板底座一次性内置仪表盘 + 主数据导入**（PRD §8.3.1 / §8.12）：M2-01 必须为 M2-07 / M2-08 预留挂载点，避免回头返工
4. **`external_import` 实体生成约束**（PRD §8.12）：M2-05 不得为该类实体生成"新增 / 批量删除"按钮
5. **Dev 失败不直接抛 Owner**（PRD §8.6）：M3-01 失败路径必须接入 M3-05 通知分派
6. **数据治理前置**（PRD §10）：M7-01 / M7-03 / M7-04 与 Wave C/D 并行，而非堆到 Wave F
7. **单 PR 单工单 + base=`cursor`**（PRD §15.2）：Coding Agent 不得把多张工单塞进同一 PR；PR base 必须是 `cursor`
8. **工单字段齐全**（PRD §15.4）：每张工单必须含 `状态 / 依赖 / 关联 BACKLOG / Range / Pickup 信号 / DoD / Evidence / 不做`；缺字段视为未就绪，Agent 不得 Pickup
9. **Wave 切换闸门**（PRD §15.5）：进入下一 Wave 前，当前 Wave 所有工单必须 `done` 或显式 `blocked`
10. **Agent 停止条件**（PRD §15.6）：触发任一即停手报告，不得「凭直觉」继续

---

## Wave A · M0 基础设施

**Wave A DoD**（来自 ROADMAP §2）：
- `docker compose up` 可启动最小 Builder（OpenHands + Django + PG + 前端）
- 可访问 OpenHands 原屏与 `/tc/*` 占位页
- 可完成一次 GitLab 机器账号"分支→提交→MR"演练
- 自检脚本可输出 PG / GitLab / LLM 三项连通状态
- **pre-commit hooks 链路本地可用**（W-A-00 解锁）

### W-A-00: 修复 Poetry / pre-commit 环境（本机闸门）
- 状态：`pending`
- 依赖：无
- 关联 BACKLOG：M0-01 前置
- 范围（Range）：
  - 根 `Makefile`（`ensure-poetry-virtualenvs-path` / `install-pre-commit-hooks`）
  - `dev_config/python/.pre-commit-config.yaml`（如必要，仅微调；改动登记 UPSTREAM_PATCHES）
  - `timberclaw/docs/EXECUTION_TODO.md`、`scripts/tc_wave_a_check.sh`（开启默认 `TC_WAVE_A_RUN_PRE_COMMIT`）
- Pickup 信号：
  - 本机已安装 **Python 3.12 + Poetry 1.8+**
  - 仓库根 `.github/workflows/lint.yml` 中的 `lint-python` 当前为绿（说明 hook 配置本身没坏）
- DoD：
  - 在 macOS / Linux 干净 shell 内执行 `make install-pre-commit-hooks` 退出码 0
  - `git commit` 测试可观察到 pre-commit 触发（至少一条 hook 输出）
  - `scripts/tc_wave_a_check.sh` 默认（不需 `TC_WAVE_A_RUN_PRE_COMMIT=1`）即包含 pre-commit 状态项 **或** README 显式说明在 W-A-00 完成前以 `TC_WAVE_A_RUN_PRE_COMMIT=1` 触发
- Evidence（PR 必跑）：
  - `python3.12 --version && poetry --version`
  - `make install-pre-commit-hooks`
  - `pre-commit run --all-files --config dev_config/python/.pre-commit-config.yaml`
- 不做：
  - 改动 OpenHands 原 `.pre-commit-config.yaml` 的 hook 集合（非必要不动）
  - 把 pre-commit 安装作为 `tc-backend` Docker 镜像的运行时依赖

### W-A-01: M0-01 Builder 项目脚手架
- 状态：`done`
- 依赖：无（W-A-00 仅影响 commit 前校验，不阻塞代码落地）
- 关联 BACKLOG：M0-01
- 范围（Range）：
  - `timberclaw/backend/`（Django 项目骨架）
  - `frontend/src/timberclaw/`（`/tc/*` 占位 + `dashboards/` / `master-data/` 预留目录）
  - 根 `docker-compose.yml`（新增 `postgres` + `tc-backend`）
- Pickup 信号：N/A（已 done）
- DoD（已满足）：
  - `docker compose up` 后可访问 OpenHands 原屏与 `http://127.0.0.1:3000/tc`
  - `tc-backend` 健康端点 `GET /api/health/` 返回 200
- Evidence：
  - `docker compose up --build`
  - `curl -fsS http://127.0.0.1:8000/api/health/`

### W-A-02: M0-03 LLM Gateway 抽象
- 状态：`done`
- 依赖：W-A-01
- 关联 BACKLOG：M0-03
- 范围（Range）：`timberclaw/backend/llm/`、`tc_project/{settings,urls}.py` 中 LLM 配置段
- Pickup 信号：N/A（已 done）
- DoD（已满足）：
  - `GET /api/health/llm/` 返回 `provider` 与密钥就绪状态
  - `POST /api/llm/invoke/`（Session 登录后）能跑通 mock，写入 `LLMCallLog`
- Evidence：
  - `docker compose run --rm tc-backend python -m pytest timberclaw/backend/tests/test_llm_gateway.py timberclaw/backend/tests/test_redact.py`
  - `curl -fsS http://127.0.0.1:8000/api/health/llm/`
- 后续接驳：Wave G 指标看板将读取 `LLMCallLog` 聚合（W-G-00 已登记）

### W-A-03: M0-04 GitLab 接入
- 状态：`done`
- 依赖：W-A-01
- 关联 BACKLOG：M0-04
- 范围（Range）：`timberclaw/backend/gitlab_integration/`、`tc_project/urls.py` 中 GitLab 路由 / 设置
- Pickup 信号：N/A（已 done）
- DoD（已满足）：
  - `GET /api/health/gitlab/` 在未配置时 `status=skipped`，配置后 `status=ok` 并返回 GitLab 版本
  - `POST /api/gitlab/smoke-write/` 在 `TC_GITLAB_ENABLE_WRITE=1` + Platform Engineer 角色下能创建分支 / 单文件提交 / 打 MR
- Evidence：
  - `docker compose run --rm tc-backend python -m pytest timberclaw/backend/tests/test_gitlab_integration.py`
  - 真实 GitLab 演练（可选）：登录 `tc_platform_engineer`，`curl -X POST http://127.0.0.1:8000/api/gitlab/smoke-write/`

### W-A-04: M0-05 Builder 部署与自检
- 状态：`done`
- 依赖：W-A-01 / W-A-02 / W-A-03（均 `done`）；W-A-00 仅影响默认是否跑 pre-commit
- 关联 BACKLOG：M0-05
- 范围（Range）：
  - `scripts/tc_wave_a_check.sh`、`scripts/tc_compose_health.sh`
  - `docker-compose.yml` 环境变量段
  - `timberclaw/README.md` 与 `timberclaw/backend/README.md`「30 min deploy」段落
  - `.github/workflows/timberclaw-builder.yml`（已建立，可微调）
- Pickup 信号：
  - `tc_wave_a_check.sh` 已含 PG TCP + API 三件套 + 可选 pytest/pre-commit
  - `.github/workflows/timberclaw-builder.yml` 已合入并在 `cursor` 触发
- DoD（已满足）：
  - `bash scripts/tc_wave_a_check.sh` 在已 `docker compose up postgres tc-backend` 后退出码 0，输出包含 `OK: postgres` / `OK: tc-backend health` / `status=skipped|ok`（GitLab）
  - `timberclaw-builder.yml` 三个 job 全绿（在 PR → `cursor` 上）
  - `timberclaw/README.md` 含 **「30 分钟部署」** 步骤清单（compose up → seed users → wave-a check → 可选 pytest）
  - **pre-commit 默认路径**：README 已写明 W-A-00 完成前用 `TC_WAVE_A_RUN_PRE_COMMIT=1`；CI 由 `lint.yml` 覆盖；W-A-00 `done` 后再评估是否把 pre-commit 并入 `tc_wave_a_check.sh` 默认
- Evidence：
  - `docker compose up -d postgres tc-backend && bash scripts/tc_wave_a_check.sh`
  - `docker compose run --rm tc-backend python -m pytest`
- 不做：
  - 在脚本中加入对生成系统（输出物）的探测（属于 Wave C 之后）

### W-A-05: M0-02 认证与账号
- 状态：`done`
- 依赖：W-A-01
- 关联 BACKLOG：M0-02
- 范围（Range）：`timberclaw/backend/accounts/`、`tc_project/{settings,urls}.py` 中 auth/DRF 段
- Pickup 信号：N/A（已 done）
- DoD（已满足）：
  - 五角色 `UserProfile`（Owner / Reviewer / Admin / PE / Human Developer）落地
  - `POST /api/auth/login/` Session 登录 + `GET /api/me/` 返回角色
  - `manage.py seed_builder_demo_users` 一键种子
- Evidence：
  - `docker compose run --rm tc-backend python -m pytest timberclaw/backend/tests/test_accounts.py`
- 注意：业务使用者（End User，PRD §4.6）**不**在 Builder 账号体系内，仅在生成系统运行时存在

---

## Wave B · M1 Spec 管道

**Wave B DoD**（来自 ROADMAP §2）：
- 同一份 spec 在"业务场景视图 + 结构化专业视图"可双向联动
- 未确认 spec 无法进入生成流程
- diff 可同时产出"业务摘要"和"结构化差异"
- **Owner UI 中无未经映射的工程术语**（W-B-00 拦截）

### W-B-00: 概念隔离最小子集前置（V1.5 关键修订）
- 状态：`done`
- 依赖：W-A-01（M0-01 脚手架）；W-A-04（M0-05 文档 / CI）
- 关联 BACKLOG：M4-06 最小子集（提前到 Wave B）
- 范围（Range）：
  - `frontend/src/timberclaw/i18n/`（新建：术语键值表 + 角色上下文 hook）
  - `frontend/src/timberclaw/`（业务屏改用 i18n 键，不再写硬编码工程词）
  - `frontend/.eslintrc`（新增局部规则）或新建 `frontend/eslint-plugin-timberclaw/`
  - `timberclaw/docs/CONVENTIONS.md` §术语映射小节（如必要）
- Pickup 信号：
  - W-A-04 已 `done`（README「30 分钟部署」+ `timberclaw-builder.yml` CI）
  - PRD §7.4 表存在并稳定（已就绪）
- DoD（已满足）：
  - i18n 键覆盖 PRD §7.4 全部映射项（含 `commit_sha` / `pr_mr` / `preview_deploy` / `prod_release` / `dev_failure` / `agent_patch` / **库表演进（键名 `ddl_change`，避免源码字面量 `migration` 误触发 ESLint）** / `rollback` / `spec_diff` + `formatReleaseCandidateLabel`）
  - ESLint：`merge request` / `pull request` / `rc-` / `commit` / `migration` / `diff` / `Preview` / `Prod` / `PR ` 及 JSXText 中 `merge request` / `commit`；`frontend/src/timberclaw/**` 现有屏 0 报错
  - `cd frontend && npm run typecheck` 通过
  - `/tc` 首页 **Descriptions** 作为「文本对照表」验收载体（替代截图）
- Evidence：
  - `cd frontend && npx eslint src/timberclaw --ext .ts,.tsx`
  - `cd frontend && npm run typecheck`
- 不做（留给 W-E-02 完整 M4-06）：
  - 候选版本 / Preview / 发布 / 反馈 全量文案
  - Reviewer 严格映射（依赖 M4-03 Preview 落地）
  - 生成系统侧错误模板统一映射

### W-B-01: M1-01 ~ M1-03（需求输入 + 初始 spec + 对话修订）
- 状态：`pending`
- 依赖：W-A-04（Wave A 收口）、W-A-05（认证）、W-B-00（术语映射，否则 UI 文案违规）
- 关联 BACKLOG：M1-01 / M1-02 / M1-03
- 范围（Range）：
  - **后端**：`timberclaw/backend/specs/`（新增 Django app：`SpecDocument` / `SpecVersion` 模型 + DRF 路由）
  - **后端**：复用 `llm.gateway.invoke()` 做 Spec Analyst 调用
  - **前端**：`frontend/src/timberclaw/specs/`（需求输入中心 + 初始 spec 业务场景视图 + 对话修订）
- Pickup 信号：
  - W-A-04 `done`、W-A-05 `done`、W-B-00 `done`
  - `POST /api/llm/invoke/` 在 mock provider 下可用
- DoD（建议拆 3 个 PR，每 PR 一个 Mn）：
  - **M1-01**：四种入口（上传 / 文本 / 对话 / 模板）任一可创建 `SpecDocument` 草稿；`pytest` 覆盖创建路径
  - **M1-02**：Spec Analyst 调 LLM 产出**业务场景视图**（角色 / 触发 / 主路径 / 异常 / 指标）；默认视图必须是业务场景视图（PRD V1.5 强约束 #2）
  - **M1-03**：对话改写 → 新 `SpecVersion`；可看 diff（业务摘要 + 结构差异，diff 摘要可在 M1-06 完善）
- Evidence：
  - `docker compose run --rm tc-backend python -m pytest timberclaw/backend/tests/test_specs.py`（新建测试）
  - `cd frontend && npx eslint src/timberclaw/specs --ext .ts,.tsx && npm run typecheck`
- 不做：
  - 结构化专业视图编辑器（M1-04，归 W-B-02）
  - Spec 显式确认闸门（M1-05，归 W-B-03）

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

## 并行智能体编排（每个角色的「当前 Pickup 候选」）

> Agent 必须按 PRD §15.3 的优先级挑工单；下面只是按「领域」给出建议候选，**实际状态以工单段为准**。

### Agent-Backend
- 负责：`timberclaw/backend/`（Django Builder API、authn/authz、LLM/GitLab 适配层、specs 模型）
- 当前 Pickup 候选：**W-B-01**（依赖 W-A-04 / W-A-05 / W-B-00，均已 `done`）
- 已完成：W-A-01 / W-A-02 / W-A-03 / W-A-05

### Agent-Frontend
- 负责：`frontend/src/timberclaw/` 业务屏（Ant Design v5）+ i18n 术语映射
- 当前 Pickup 候选：**W-B-01**（需求输入中心 UI + 调后端 spec API）
- 已完成：W-A-01 `/tc/*` 占位；**W-B-00** 术语映射 + ESLint 守卫

### Agent-Infra
- 负责：根 `docker-compose.yml`、`scripts/`、CI workflow、环境变量约定
- 当前 Pickup 候选：**W-A-00**（本机 `make install-pre-commit-hooks`）
- 已完成：`postgres` + `tc-backend` + `tc_compose_health.sh` + `tc_wave_a_check.sh` + `.github/workflows/timberclaw-builder.yml` + README「30 分钟部署」

### Agent-QA
- 负责：验收清单、命令验证、阻塞与风险归档
- 当前 Pickup 候选：在每张被推进的工单 PR 中执行 `Evidence` 命令并粘贴输出；对 `EXECUTION_TODO.md` 字段缺失的工单提「字段补齐」小 PR
- 已完成：将 W-A-* 已交付工单字段化（按 PRD §15.4）

---

## 风险与阻塞

1. **W-A-00**（pre-commit 本机闸门）：仓库级 lint 已由 `.github/workflows/lint.yml` 的 `lint-python`（pip 安装方式）覆盖，PR 仍受拦截；本机 `make install-pre-commit-hooks` 仍待 Python 3.12 + Poetry 环境复验后标 `done`。**不阻塞 Wave A 收口的 CI 验证，但阻塞「30 min deploy」叙事完整性**。
2. **依赖图风险**：M7-01 / M7-03 / M7-04 已前移到 W-C-Aux；若 Wave C 漏做，Wave F 的 M6-01 无法启动（M6-01 强依赖 M7-04 操作日志）。
3. **Wave A 收尾**：M0-01 ~ M0-04 与 **M0-05（W-A-04）** 已交付；仅剩 **W-A-00** 本机 pre-commit 闸门。M1~M8 仍不得越级（PRD §15.5）。
4. **Vitest 全仓现状**：`npx vitest run` 在仓库层有上百例既有失败（OpenHands 上游测试 / 环境问题），**与 TimberClaw 后端无关**；TimberClaw 前端工单的 Evidence 仅要求对应子树的 vitest（如有），不要求全仓 vitest 通过。

---

## 下一步（Next Action，按 PRD §15.3 顺序）

1. **W-B-01**：落地 `timberclaw/backend/specs/` + `frontend/src/timberclaw/specs/`（M1-01~03 最小切片）；PR base `cursor`。
2. **W-A-00**（并行）：本机 Python 3.12 + Poetry 跑通 `make install-pre-commit-hooks` → 标 `done` → 再评估 `tc_wave_a_check.sh` 默认 pre-commit。
3. **PR 合并节奏**：保持 **单 PR 单工单**（PRD §15.2）；超过 5 批次的工单必须拆。

---

## 更新规则（V1.6）

每次工单状态变更或 PR 合并后，**必须**更新以下字段，且对每张工单**保持 PRD §15.4 规定的字段齐全**：

1. 工单状态（`pending` / `in_progress` / `blocked` / `done`）
2. 当前批次（Batch）与 commit / PR 链接
3. 「风险与阻塞」（新增 / 解除）
4. 「下一步（Next Action）」按 §15.3 重新排序
5. **PRD V1.6 强约束区**：若新发现强约束，追加并标注影响的 Wave

> **缺字段视为工单未就绪**（PRD §15.4），Coding Agent 不得 Pickup；遇此情况由 Agent 提交「字段补齐」小 PR，再 Pickup。
