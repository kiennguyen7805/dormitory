import { Card, Col, Row, Tag, Typography } from 'antd'

import { useAuth } from '../../auth/AuthContext'

export default function StudentHome() {
  const { user } = useAuth()
  return (
    <div>
      <Typography.Title level={2}>Xin chào, {user?.full_name}</Typography.Title>
      <Typography.Paragraph type="secondary">Tài khoản sinh viên đã đăng nhập thành công.</Typography.Paragraph>
      <Row gutter={16}>
        <Col xs={24} md={8}><Card title="Vai trò"><Tag color="blue">Student</Tag></Card></Col>
        <Col xs={24} md={8}><Card title="Đăng ký ở">Sẽ triển khai ở tuần 2</Card></Col>
        <Col xs={24} md={8}><Card title="Hóa đơn">Sẽ triển khai ở tuần 3</Card></Col>
      </Row>
    </div>
  )
}
