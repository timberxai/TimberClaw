# TimberClaw 执行看板（实时 Todo）

> 目标：把“分阶段推进 + 实时状态更新 + 可并行拆分”落地为统一看板。
>
> 状态定义：`pending`（未开始）/ `in_progress`（进行中）/ `blocked`（阻塞）/ `done`（完成）

## 更新时间
- 2026-04-18 (UTC)

## 当前总览
- 当前波次：**Wave A（M0 基础设施）**
- 当前 Sprint：**Sprint-0（M0-01 优先）**
- 总计划：见 `timberclaw/docs/ROADMAP_EXECUTION_PLAN.md`
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
  - Batch 2：仓库与目录落位初始化（进行中）
  - Batch 3：运行与连通性自检（待开始）

### W-A-02: M0-03 LLM Gateway 抽象
- 状态：`pending`
- 依赖：M0-01
- 并行策略：M0-01 完成后与 W-A-03 并行

### W-A-03: M0-04 GitLab 接入
- 状态：`pending`
- 依赖：M0-01
- 并行策略：M0-01 完成后与 W-A-02 并行

### W-A-04: M0-05 Builder 部署与自检
- 状态：`pending`
- 依赖：M0-01、M0-03、M0-04
- 并行策略：作为 Wave A 收口工单

### W-A-05: M0-02 认证与账号
- 状态：`pending`
- 依赖：M0-01
- 并行策略：可在 M0-01 后与 W-A-02/03 交错推进

---

## Wave B~G 预备队列（持续推进）

### Wave B（M1）
- W-B-01: M1-01~M1-03（需求输入 + 初始 spec + 对话修订）`pending`
- W-B-02: M1-04~M1-06（结构化编辑 + 确认闸门 + 双视图）`pending`

### Wave C（M2）
- W-C-01: M2-01~M2-03（前后端模板 + 部署模板）`pending`
- W-C-02: M2-04~M2-06（实现计划 + 首次生成 + fixtures）`pending`
- W-C-03: M2-07~M2-08（仪表盘 + 主数据导入导出）`pending`

### Wave D（M3）
- W-D-01: M3-01~M3-03（验证编排 + 自动修复 + 风险识别）`pending`
- W-D-02: M3-04~M3-05（MR 自动化 + 失败分派）`pending`

### Wave E（M4+M5）
- W-E-01: M4-01~M4-06（候选版本 + Preview + 术语映射）`pending`
- W-E-02: M5-01~M5-05（反馈→patch 闭环）`pending`

### Wave F（M6+M7）
- W-F-01: M6-01~M6-03（发布 + 回滚）`pending`
- W-F-02: M7-01~M7-06（数据治理 + 审计）`pending`

### Wave G（M8）
- W-G-01: M8-01~M8-05（端到端冒烟 + 指标看板）`pending`

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
- 说明：维护执行看板与总计划文档

---

## 风险与阻塞

1. `make install-pre-commit-hooks` 在当前环境失败：
   - 错误：`No such file or directory: /root/.cache/pypoetry/virtualenvs/envs.toml`
   - 影响：pre-commit hooks 未能完成安装
   - 策略：记录失败并继续执行“能跑的都跑”的检查；后续补齐 Poetry 环境后重试

2. M0 尚未完成，M1~M8 只能做计划与队列管理，不能越级实现依赖工单。

---

## 下一步（Next Action）

1. 进入 M0-01 Batch 2：落地最小路由骨架（`/tc/*`）与 Django 目录骨架。
2. 衔接 M0-01 Batch 3：验证 compose 启动链路并记录证据。
3. M0-01 达标后，按并行策略同时拉起 M0-02 / M0-03 / M0-04。

---

## 更新规则

每次任务反馈时，必须更新以下字段：
1. 任务状态（pending/in_progress/blocked/done）
2. 当前批次（Batch）与完成结果
3. 风险与阻塞（新增/解除）
4. 下一步（Next Action）
