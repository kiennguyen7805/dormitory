import { Card, Descriptions, Empty, Table, Tag, Typography, message } from 'antd'
import { useCallback, useEffect, useState } from 'react'

import { apiRequest } from '../../api/client'
import type { BedAssignment, Contract } from './types'

export default function MyHousingPage() {
  const [contract, setContract] = useState<Contract | null>(null)
  const [history, setHistory] = useState<BedAssignment[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const data = await apiRequest<Contract | null>('/contracts/me')
      setContract(data)
      setHistory(data ? await apiRequest<BedAssignment[]>(`/contracts/${data.id}/assignment-history`) : [])
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không tải được chỗ ở')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void load() }, [load])

  if (!loading && !contract) {
    return <Card><Empty description="Bạn chưa có hợp đồng ký túc xá" /></Card>
  }

  return <div>
    <Typography.Title level={2}>Chỗ ở của tôi</Typography.Title>
    {contract && <Card style={{ marginBottom: 16 }}>
      <Descriptions title={contract.contract_no} bordered column={{ xs: 1, md: 2 }}>
        <Descriptions.Item label="Trạng thái"><Tag color={contract.status === 'Active' ? 'green' : 'default'}>{contract.status}</Tag></Descriptions.Item>
        <Descriptions.Item label="Thời hạn">{contract.start_date} — {contract.end_date}</Descriptions.Item>
        <Descriptions.Item label="Phí ở">{Number(contract.base_rate).toLocaleString('vi-VN')} đ/tháng</Descriptions.Item>
        <Descriptions.Item label="Giường hiện tại">
          {contract.current_assignment
            ? `${contract.current_assignment.building_code}-${contract.current_assignment.room_code} / ${contract.current_assignment.bed_code}`
            : 'Không có'}
        </Descriptions.Item>
      </Descriptions>
    </Card>}
    <Card title="Lịch sử ở">
      <Table rowKey="id" loading={loading} dataSource={history} columns={[
        { title: 'Tòa', dataIndex: 'building_code' },
        { title: 'Phòng', dataIndex: 'room_code' },
        { title: 'Giường', dataIndex: 'bed_code' },
        { title: 'Từ ngày', dataIndex: 'start_date' },
        { title: 'Đến ngày', dataIndex: 'end_date', render: (value) => value ?? 'Hiện tại' },
        { title: 'Trạng thái', dataIndex: 'status', render: (value) => <Tag color={value === 'Active' ? 'green' : 'default'}>{value}</Tag> },
      ]} />
    </Card>
  </div>
}
