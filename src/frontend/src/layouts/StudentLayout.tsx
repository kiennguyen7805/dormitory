import { LogoutOutlined, UserOutlined } from '@ant-design/icons'
import { Avatar, Button, Layout, Menu, Space, Typography } from 'antd'
import { Outlet, useNavigate } from 'react-router-dom'
import { useLocation } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext'

const { Header, Content } = Layout

export default function StudentLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  return (
    <Layout className="app-shell">
      <Header className="topbar student-topbar">
        <Space size={24}>
          <Typography.Title level={4}>Cổng thông tin Sinh viên</Typography.Title>
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            onClick={({ key }) => navigate(key)}
            items={[
              { key: '/student', label: 'Trang chủ' },
              { key: '/student/applications', label: 'Đăng ký ở KTX' },
              { key: '/student/my-housing', label: 'Chỗ ở của tôi' },
            ]}
          />
        </Space>
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
