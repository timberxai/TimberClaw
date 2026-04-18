import { Card, Typography } from "antd";

export default function TcMasterData() {
  return (
    <Card title="主数据（占位）">
      <Typography.Paragraph>
        按 PRD §8.12，物料、工作中心、员工、班组等主数据将在此通过 CSV / Excel
        单向导入维护；此处仅预留路由与页面壳。
      </Typography.Paragraph>
    </Card>
  );
}
