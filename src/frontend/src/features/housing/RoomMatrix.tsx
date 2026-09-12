import { ApartmentOutlined } from '@ant-design/icons'
import { Card, Col, Empty, Row, Space, Spin, Tag, Typography, message } from 'antd'
import { useEffect, useState } from 'react'

import { apiRequest } from '../../api/client'
import type { MatrixBuilding } from './types'

const statusColor = { Available: 'green', Occupied: 'red', Maintenance: 'orange' }
const statusLabel = { Available: 'Còn trống', Occupied: 'Đã có người', Maintenance: 'Bảo trì' }

export default function RoomMatrix() {
  const [data, setData] = useState<MatrixBuilding[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => { apiRequest<MatrixBuilding[]>('/room-matrix').then(setData).catch((e) => message.error(e.message)).finally(() => setLoading(false)) }, [])
  if (loading) return <Spin fullscreen tip="Đang tải sơ đồ..." />
  return <div><Typography.Title level={2}>Sơ đồ phòng/giường</Typography.Title><Typography.Paragraph type="secondary">F05: trạng thái giường được suy ra tự động, không nhập thủ công.</Typography.Paragraph>
    {!data.length ? <Empty description="Chưa có dữ liệu. Hãy tạo tòa, phòng và giường trước." /> : data.map(building => <Card key={building.id} title={<Space><ApartmentOutlined />{building.code} — {building.name}</Space>} style={{ marginBottom: 20 }}>
      <Row gutter={[16, 16]}>{building.rooms.map(room => <Col xs={24} md={12} xl={8} key={room.id}><Card size="small" title={`Phòng ${room.code} · Tầng ${room.floor}`} extra={room.room_type}>
        <Space wrap>{room.beds.map(bed => <Tag key={bed.id} color={statusColor[bed.status]}>{bed.code}: {statusLabel[bed.status]}</Tag>)}</Space>
      </Card></Col>)}</Row>
    </Card>)}
  </div>
}
