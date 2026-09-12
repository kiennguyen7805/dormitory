import { LogoutOutlined, UserOutlined } from '@ant-design/icons'
import { Avatar, Button, Layout, Space, Typography } from 'antd'
import { Outlet, useNavigate } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext'

const { Header, Content } = Layout

export default function StudentLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  return (
    <Layout className="app-shell">
      <Header className="topbar student-topbar">
        <Typography.Title level={4}>Cổng thông tin Sinh viên</Typography.Title>
        <Space>
          <Avatar icon={<UserOutlined />} />
          <Typography.Text>{user?.full_name}</Typography.Text>
          <Button icon={<LogoutOutlined />} onClick={async () => { await logout(); navigate('/login') }}>Đăng xuất</Button>
        </Space>
      </Header>
      <Content className="page-content"><Outlet /></Content>
    </Layout>
  )
}
