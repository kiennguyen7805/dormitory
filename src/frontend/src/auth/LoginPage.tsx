import { LockOutlined, MailOutlined } from '@ant-design/icons'
import { Alert, Button, Card, Form, Input, Segmented, Space, Typography, message } from 'antd'
import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'

import { useAuth } from './AuthContext'
import type { Role } from './types'

const demoAccounts: Record<Role, { email: string; password: string }> = {
  Admin: { email: 'admin@dormitory.local', password: 'Admin@123' },
  Staff: { email: 'staff@dormitory.local', password: 'Staff@123' },
  Student: { email: 'student@dormitory.local', password: 'Student@123' },
}

export default function LoginPage() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [selectedRole, setSelectedRole] = useState<Role>('Admin')
  const [form] = Form.useForm()

  if (user) return <Navigate to={user.role === 'Student' ? '/student' : '/admin/housing'} replace />

  const applyDemo = (role: Role) => {
    setSelectedRole(role)
    form.setFieldsValue(demoAccounts[role])
  }

  const submit = async (values: { email: string; password: string }) => {
    setLoading(true)
    try {
      const loggedInUser = await login(values.email, values.password)
      message.success(`Đăng nhập với vai trò ${loggedInUser.role}`)
      navigate(loggedInUser.role === 'Student' ? '/student' : '/admin/housing')
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Đăng nhập thất bại')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <Card className="login-card">
        <Space direction="vertical" size={18} style={{ width: '100%' }}>
          <div>
            <Typography.Title level={2}>Quản lý Ký túc xá</Typography.Title>
            <Typography.Text type="secondary">Đăng nhập để tiếp tục vào hệ thống</Typography.Text>
          </div>
          <Alert message="Tài khoản demo tuần 1" description="Chọn vai trò để tự điền tài khoản đã seed." type="info" showIcon />
          <Segmented<Role>
            block
            value={selectedRole}
            options={['Admin', 'Staff', 'Student']}
            onChange={applyDemo}
          />
          <Form form={form} layout="vertical" initialValues={demoAccounts.Admin} onFinish={submit}>
            <Form.Item name="email" label="Email" rules={[{ required: true }, { type: 'email' }]}>
              <Input prefix={<MailOutlined />} size="large" />
            </Form.Item>
            <Form.Item name="password" label="Mật khẩu" rules={[{ required: true }]}>
              <Input.Password prefix={<LockOutlined />} size="large" />
            </Form.Item>
            <Button type="primary" htmlType="submit" size="large" block loading={loading}>
              Đăng nhập
            </Button>
          </Form>
        </Space>
      </Card>
    </div>
  )
}
