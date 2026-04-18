# TimberClaw 执行看板（实时 Todo）

> 目标：把“分阶段推进 + 实时状态更新 + 可并行拆分”落地为统一看板。
>
> 状态定义：`pending`（未开始）/ `in_progress`（进行中）/ `blocked`（阻塞）/ `done`（完成）

## 更新时间
- 2026-04-18 (UTC)

## 当前总览
- 当前波次：**Wave A（M0 基础设施）**
- 当前 Sprint：**Sprint-0（M0-01 优先）**
- 下一里程碑出口：`docker compose up` 可拉起 Builder 基础能力

---

## Wave A · M0 基础设施

### W-A-01: M0-01 Builder 项目脚手架
- 状态：`in_progress`
- 依赖：无
- 关联 BACKLOG：M0-01
- 范围摘要：
  - 在 OpenHands fork 基础上叠加 TimberClaw 业务模块骨架
  - 打通 `/tc/*` 路由占位与基础布局入口
  - 扩展 compose 以纳入 Django + PostgreSQL（按最小侵入策略）
- 本次执行批次（Batch）
  - Batch 1：计划与任务切分（完成）
  - Batch 2：仓库与目录落位初始化（待开始）
  - Batch 3：运行与连通性自检（待开始）

### W-A-02: M0-03 LLM Gateway 抽象
- 状态：`pending`
- 依赖：M0-01
- 并行策略：可在 M0-01 基础骨架稳定后并行

### W-A-03: M0-04 GitLab 接入
- 状态：`pending`
- 依赖：M0-01
- 并行策略：可与 W-A-02 并行

### W-A-04: M0-05 Builder 部署与自检
- 状态：`pending`
- 依赖：M0-01、M0-03、M0-04
- 并行策略：作为 Wave A 收口工单

### W-A-05: M0-02 认证与账号
- 状态：`pending`
- 依赖：M0-01
- 并行策略：可在 M0-01 之后与 W-A-02/03 交错推进

---

## 并行智能体编排

### Agent-Backend
- 负责：Django 项目骨架、后端配置、API 占位
- 当前状态：`pending`

### Agent-Frontend
- 负责：`frontend/src/timberclaw/` 路由挂载与 AntD 占位页
- 当前状态：`pending`

### Agent-Infra
- 负责：compose 扩展、自检脚本、环境变量约定
- 当前状态：`pending`

### Agent-QA
- 负责：验收清单、命令验证、阻塞与风险归档
- 当前状态：`in_progress`
- 说明：正在维护本看板与 Sprint 计划

---

## 风险与阻塞

- `make install-pre-commit-hooks` 在当前环境因 Poetry 拉取依赖访问 pypi.org 失败而中断。
- 处理策略：
  1. 已执行命令并记录失败日志；
  2. 后续改动继续执行“能跑的都跑”的本地检查；
  3. 网络恢复后重试 hooks 安装。

---

## 更新规则

每次任务反馈时，必须更新以下字段：
1. 任务状态（pending/in_progress/blocked/done）
2. 当前批次（Batch）与完成结果
3. 风险与阻塞（新增/解除）
4. 下一步（Next Action）
