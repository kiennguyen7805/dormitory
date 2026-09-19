import { ApartmentOutlined, FileProtectOutlined, LogoutOutlined, UserOutlined } from '@ant-design/icons'
import { Avatar, Button, Layout, Menu, Space, Typography } from 'antd'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext'

const { Header, Sider, Content } = Layout

export default function AdminLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const onLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <Layout className="app-shell">
      <Sider breakpoint="lg" collapsedWidth="0" width={250}>
        <div className="brand">KTX Manager</div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          onClick={({ key }) => navigate(key)}
          items={[
            { key: '/admin/housing', icon: <ApartmentOutlined />, label: 'Cơ sở vật chất' },
            { key: '/admin/room-matrix', icon: <ApartmentOutlined />, label: 'Sơ đồ phòng/giường' },
            { key: '/admin/applications', icon: <FileProtectOutlined />, label: 'Đăng ký & hợp đồng' },
          ]}
        />
      </Sider>
      <Layout>
        <Header className="topbar">
          <Typography.Text strong>Quản lý ký túc xá</Typography.Text>
          <Space>
            <Avatar icon={<UserOutlined />} />
            <div className="user-summary">
              <Typography.Text strong>{user?.full_name}</Typography.Text>
              <Typography.Text type="secondary">{user?.role}</Typography.Text>
            </div>
            <Button icon={<LogoutOutlined />} onClick={onLogout}>Đăng xuất</Button>
          </Space>
        </Header>
        <Content className="page-content"><Outlet /></Content>
      </Layout>
    </Layout>
  )
}
