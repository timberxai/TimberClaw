/**
 * Owner / Reviewer 可见文案的工程术语映射（PRD §7.4 最小子集）。
 * W-B-00：集中维护；业务屏禁止散落硬编码工程英文词。
 */

export type BuilderUiRole = "owner" | "reviewer";

/** 映射键：与 PRD §7.4 行一一对应（不含需动态编号的占位，另见 format 函数）。 */
export type BuilderTerminologyKey =
  | "pr_mr"
  | "preview_deploy"
  | "prod_release"
  | "dev_failure"
  | "agent_patch"
  | "migration"
  | "rollback"
  | "spec_diff";

const OWNER: Record<BuilderTerminologyKey, string> = {
  pr_mr: "修改集",
  preview_deploy: "开启在线试用 / 试用环境",
  prod_release: "正式启用 / 上线",
  dev_failure: "系统自检发现问题",
  agent_patch: "系统自动修改",
  migration: "数据结构调整",
  rollback: "撤回到上一个版本",
  spec_diff: "需求变化摘要",
};

const REVIEWER: Record<BuilderTerminologyKey, string> = {
  pr_mr: "（隐藏）",
  preview_deploy: "试用系统",
  prod_release: "系统更新",
  dev_failure: "（隐藏）",
  agent_patch: "（隐藏）",
  migration: "（隐藏）",
  rollback: "系统已还原为上一个版本",
  spec_diff: "版本变化说明",
};

export function builderTerminology(
  key: BuilderTerminologyKey,
  role: BuilderUiRole = "owner",
): string {
  return role === "owner" ? OWNER[key] : REVIEWER[key];
}

/** 候选版本 rc-N → 产品用语（PRD §7.4）。 */
export function formatReleaseCandidateLabel(
  rcNumber: number,
  role: BuilderUiRole = "owner",
): string {
  if (role === "owner") {
    return `版本 #${rcNumber} / 试用版 ${rcNumber}`;
  }
  return `版本 ${rcNumber}`;
}
