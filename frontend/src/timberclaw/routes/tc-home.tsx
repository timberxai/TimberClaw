import { Alert, Card, Descriptions, Space, Typography } from "antd";

import { builderTerminology, formatReleaseCandidateLabel } from "../i18n";

export default function TcHome() {
  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <Typography.Title level={3}>欢迎使用 TimberClaw</Typography.Title>
      <Alert
        type="info"
        showIcon
        message="为工厂信息化负责人设计"
        description="这里将承载需求整理、业务场景确认、试用版本与正式启用等流程。当前为占位界面，用于验证路由与布局。"
      />
      <Card title="产品用语映射（W-B-00 骨架）" variant="borderless">
        <Typography.Paragraph type="secondary">
          下列词条来自 PRD §7.4，由{" "}
          <Typography.Text code>frontend/src/timberclaw/i18n/</Typography.Text>{" "}
          集中导出，避免在业务屏硬编码工程英文词。
        </Typography.Paragraph>
        <Descriptions column={1} size="small" bordered>
          <Descriptions.Item label="修改集（工程侧 MR，Owner 映射）">
            {builderTerminology("pr_mr", "owner")}
          </Descriptions.Item>
          <Descriptions.Item label="试用环境部署（Owner 映射）">
            {builderTerminology("preview_deploy", "owner")}
          </Descriptions.Item>
          <Descriptions.Item label="正式上线（Owner 映射）">
            {builderTerminology("prod_release", "owner")}
          </Descriptions.Item>
          <Descriptions.Item label="候选版本编号示例（#3，Owner 映射）">
            {formatReleaseCandidateLabel(3, "owner")}
          </Descriptions.Item>
          <Descriptions.Item label="试用环境（Reviewer 映射）">
            {builderTerminology("preview_deploy", "reviewer")}
          </Descriptions.Item>
        </Descriptions>
      </Card>
      <Card title="下一步（工程）" variant="borderless">
        <Typography.Paragraph>
          后端健康检查：<Typography.Text code>/api/health/</Typography.Text>
          （Docker 中默认映射端口 8000）。OpenHands 对话与代码能力仍在原有入口。
        </Typography.Paragraph>
      </Card>
    </Space>
  );
}
