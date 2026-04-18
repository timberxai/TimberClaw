import { ConfigProvider, Layout, Menu, Typography, theme } from "antd";
import zhCN from "antd/locale/zh_CN";
import { Link, Outlet, useLocation } from "react-router";
import "antd/dist/reset.css";

const { Header, Content } = Layout;

function TcShell() {
  const location = useLocation();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const selected = (() => {
    if (location.pathname.startsWith("/tc/dashboards"))
      return ["/tc/dashboards"];
    if (location.pathname.startsWith("/tc/master-data"))
      return ["/tc/master-data"];
    return ["/tc"];
  })();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center", gap: 24 }}>
        <Typography.Title level={4} style={{ margin: 0, color: "#fff" }}>
          TimberClaw 工厂业务搭建
        </Typography.Title>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={selected}
          style={{ flex: 1, minWidth: 0 }}
          items={[
            { key: "/tc", label: <Link to="/tc">工作台</Link> },
            {
              key: "/tc/dashboards",
              label: <Link to="/tc/dashboards">仪表盘</Link>,
            },
            {
              key: "/tc/master-data",
              label: <Link to="/tc/master-data">主数据</Link>,
            },
          ]}
        />
      </Header>
      <Content style={{ padding: 24, background: colorBgContainer }}>
        <Outlet />
      </Content>
    </Layout>
  );
}

export default function TcRootLayout() {
  return (
    <ConfigProvider locale={zhCN}>
      <TcShell />
    </ConfigProvider>
  );
}
