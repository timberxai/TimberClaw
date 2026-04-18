# TimberClaw-code

> 基于 [OpenHands](https://github.com/All-Hands-AI/OpenHands) fork 改造的工业业务系统 Builder。
>
> 让工厂信息化负责人从业务场景对话出发，先生成并确认 spec，再在受约束的模板底座内自动生成系统，在 Preview 中体验和反馈，在人工把关下发布到 Prod，最终由不懂代码的车间 / 排产 / 质检人员日常使用。

---

## 仓库身份

- **这是什么**：OpenHands 的一个 fork，TimberClaw-code 的 monorepo
- **目标**：产出一个能够为离散制造工厂生成轻量 MES / BI 系统的 Builder
- **上游**：<https://github.com/All-Hands-AI/OpenHands>（MIT 协议）
- **默认分支**：`main`（受保护）

本 README 是 `timberclaw/` 子目录的入口。仓库顶层的 [`README.md`](../README.md) 是 TimberClaw-code 整个项目的门面，按需回看。上游 OpenHands 原始的开发指南仍保留在根 [`AGENTS.md`](../AGENTS.md) 和 [`Development.md`](../Development.md) 等文件里，作为开发环境参考。

---

## 文档入口（阅读顺序）

所有 TimberClaw-code 的产品与工程文档都在本目录下，按下面的顺序阅读：

| 顺序 | 文档 | 读者 | 内容 |
|------|------|------|------|
| 1 | [`docs/PRD.md`](docs/PRD.md) | 所有角色 | **单一真相源**。产品定义、角色、流程、默认实现、MVP 范围、成功标准 |
| 2 | [`AGENTS.md`](AGENTS.md) | Coding Agent / Human Developer | **Coding Agent 工作指南**（必读）：要做什么、不能做什么、怎么挑工单、怎么处理失败 |
| 3 | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) | 所有角色 | 仓库约定：目录纪律、分支命名、commit 规范、上游同步 |
| 4 | [`docs/BACKLOG.md`](docs/BACKLOG.md) | Coding Agent / Platform Engineer | 里程碑 M0–M8 + 50+ 张工单（含验收标准） |
| 5 | [`docs/FORK_CANDIDATES.md`](docs/FORK_CANDIDATES.md) | 参考档案 | 为什么选 OpenHands |

如果这是你第一次进入项目，建议按 1 → 2 → 3 → 4 读一遍再开始写代码。

---

## 当前状态

| 项 | 状态 |
|----|------|
| PRD | **V1.5**（对齐离散制造真实场景 + 概念隔离 + 仪表盘一等公民 + CSV 主数据 + 双视图） |
| BACKLOG | **V1.2**（对齐 PRD V1.5，新增 5 张核心工单） |
| 代码实现 | 尚未开始（处于 bootstrap 阶段） |
| Fork 起始 tag | 待 Platform Engineer 在 M0-01 启动时锁定并回写 PRD §2 |

---

## 角色概览

详见 PRD §4。一句话版本：

- **Owner**：工厂信息化负责人 / IT（不是开发者）
- **Reviewer**：业务使用者中参与 Preview 试用反馈的代表
- **Admin**：平台管理员 / 运维
- **Platform Engineer**：维护模板底座、Builder 运行时、LLM Gateway 的技术角色
- **Human Developer**：人工开发者（降级通道）
- **业务使用者 (End User)**：真正在车间 / 工位用系统的工厂人员；**不直接接触 Builder**

---

## 如何本地跑起来

MVP 的本地启动方式尚未搭建（属于 BACKLOG **M0-01 + M0-05**）。上游 OpenHands 的启动流程见根目录 `README.md` 和 `AGENTS.md`，供参考。

搭建完成后，启动命令预期为：

```bash
docker compose up
```

具体步骤以 M0-05 完成后的 README 为准。

---

## 贡献与协作

- 任何 Agent / 人工变更都必须通过 Git 分支 + PR，禁止直推 `main`
- 分支 / commit 命名见 [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) §4
- Agent 工作前必读 [`AGENTS.md`](AGENTS.md)

---

## 许可证

本仓库继承上游 OpenHands 的 **MIT 协议**。
