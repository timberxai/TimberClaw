import { Alert, Card, Space, Typography } from "antd";

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
      <Card title="下一步（工程）" variant="borderless">
        <Typography.Paragraph>
          后端健康检查：<Typography.Text code>/api/health/</Typography.Text>
          （Docker 中默认映射端口 8000）。OpenHands 对话与代码能力仍在原有入口。
        </Typography.Paragraph>
      </Card>
    </Space>
  );
}
