import { Button, Card, Form, Input, Select, Space, Table, Tag, Typography, message } from 'antd'
import { useCallback, useEffect, useState } from 'react'

import { apiRequest } from '../../api/client'
import type { RoomType } from '../housing/types'
import type { HousingApplication } from './types'

const statusColor = { Submitted: 'gold', Approved: 'green', Rejected: 'red' }
const statusText = { Submitted: 'Chờ duyệt', Approved: 'Đã duyệt', Rejected: 'Từ chối' }

export default function StudentApplicationsPage() {
  const [applications, setApplications] = useState<HousingApplication[]>([])
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([])
  const [loading, setLoading] = useState(true)
  const [form] = Form.useForm()

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [applicationData, roomTypeData] = await Promise.all([
        apiRequest<HousingApplication[]>('/housing-applications'),
        apiRequest<RoomType[]>('/room-types'),
      ])
      setApplications(applicationData)
      setRoomTypes(roomTypeData.filter((item) => item.is_active))
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không tải được đăng ký')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void load() }, [load])

  const submit = async (values: { term_code: string; preferred_room_type_id: string }) => {
    try {
      await apiRequest('/housing-applications', {
        method: 'POST',
        body: JSON.stringify(values),
      })
      message.success('Đã gửi đăng ký ở ký túc xá')
      form.resetFields()
      await load()
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không thể gửi đăng ký')
    }
  }

  return <div>
    <Typography.Title level={2}>Đăng ký ở ký túc xá</Typography.Title>
    <Card title="Đăng ký mới" style={{ marginBottom: 16 }}>
      <Form form={form} layout="inline" onFinish={submit}>
        <Form.Item name="term_code" label="Học kỳ" rules={[{ required: true }]}>
          <Input placeholder="VD: HK1-2026" />
        </Form.Item>
        <Form.Item name="preferred_room_type_id" label="Loại phòng mong muốn" rules={[{ required: true }]}>
          <Select style={{ width: 240 }} options={roomTypes.map((item) => ({
            value: item.id,
            label: `${item.name} - ${Number(item.default_monthly_rate).toLocaleString('vi-VN')} đ/tháng`,
          }))} />
        </Form.Item>
        <Button type="primary" htmlType="submit">Gửi đăng ký</Button>
      </Form>
    </Card>
    <Table rowKey="id" loading={loading} dataSource={applications} columns={[
      { title: 'Học kỳ', dataIndex: 'term_code' },
      { title: 'Loại phòng', dataIndex: 'preferred_room_type_name' },
      { title: 'Ngày gửi', dataIndex: 'created_at', render: (value) => new Date(value).toLocaleString('vi-VN') },
      { title: 'Trạng thái', dataIndex: 'status', render: (value: keyof typeof statusColor) => <Tag color={statusColor[value]}>{statusText[value]}</Tag> },
      { title: 'Ghi chú', render: (_, item) => <Space>{item.rejection_reason ?? '—'}</Space> },
    ]} />
  </div>
}
