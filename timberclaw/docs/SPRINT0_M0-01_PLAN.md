# Sprint-0 实施计划（M0-01）

> 对齐工单：`M0-01 Builder 项目脚手架`
>
> 目标：启动 TimberClaw 的最小可运行地基，为 M0-02 / M0-03 / M0-04 并行提供承载。

## 1. 范围与边界

### 1.1 范围（做）
1. 建立 TimberClaw 业务代码落位目录（`timberclaw/` 与 `frontend/src/timberclaw/`）
2. 在前端挂载 `/tc/*` 路由占位页（Ant Design）
3. 规划并最小化扩展 `docker-compose.yml`（必要时标记 upstream patch）
4. 确保本地可形成“OpenHands + TimberClaw 占位能力”的启动路径

### 1.2 非范围（不做）
1. 不做 CI/CD
2. 不做自动发布/多环境推送
3. 不改写 OpenHands 原有 UI 风格

## 2. 依赖

- 工单依赖：无（M0-01 为起始工单）
- 执行依赖：
  - Python/Node 基础环境
  - 可用的本地依赖安装网络（用于完整 hooks 与前后端依赖）

## 3. 执行批次

### Batch 1（已完成）
- 完成前置文档对齐（README / AGENTS / PRD / CONVENTIONS / BACKLOG）
- 完成全局蓝图与并行方案确认
- 建立实时 Todo 看板

### Batch 2（已完成）
- 目录与路由最小骨架落地（优先无侵入）
- 识别必要上游改动点并标注 `[upstream-patch]` 计划

### Batch 3（已完成）
- compose 运行链路验证（`docker compose up --build` + `scripts/tc_compose_health.sh`）
- 验收结果：OpenHands 3000、`/tc` AntD 占位、`tc-backend` `/api/health/`、Postgres 健康检查通过（由 Owner 侧确认）

### 后续（M0-02+）
- Builder 认证与角色矩阵在 `timberclaw/backend/accounts/` 演进；M0-05 统一自检脚本

## 4. 验收映射（M0-01）

工单验收要求：`docker compose up` 可启动 Builder 本体；能访问 OpenHands 原屏与 `/tc/*` 占位页。

映射到可观测项：
1. 进程启动：compose 中服务均可启动到可用状态
2. 前端访问：`/tc/*` 路由返回 AntD 占位页
3. 兼容性：不影响 OpenHands 既有入口

## 5. 并行执行分工

- Agent-Backend：后端骨架与配置
- Agent-Frontend：`/tc/*` 路由与占位页面
- Agent-Infra：compose 扩展与自检
- Agent-QA：验收映射、风险归档、看板维护

## 6. 风险清单

1. 依赖安装受环境影响（pre-commit hooks 安装失败，需修复 Poetry 缓存环境）
2. 上游目录改动可能引发冲突（需最小侵入与补丁登记）
3. 前后端版本差异导致本地编译链不稳定

## 7. 下一步

1. 完成 Batch 2：先落地 `frontend/src/timberclaw/` 路由占位
2. 补齐后端/compose 最小骨架
3. 完成 Batch 3：运行链路验证并回写看板
4. M0-01 验收后启动 M0-02 / M0-03 / M0-04 并行
