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
        <Col xs={24} md={8}><Card title="Đăng ký ở">Theo dõi đăng ký và hợp đồng tại mục Chỗ ở của tôi.</Card></Col>
        <Col xs={24} md={8}><Card title="Hồ sơ">Cập nhật thông tin sinh viên và liên hệ khẩn cấp.</Card></Col>
      </Row>
    </div>
  )
}
