import {
  Button,
  Card,
  Form,
  Input,
  Modal,
  Select,
  Space,
  Table,
  Tag,
  Typography,
  message,
} from 'antd'
import { useCallback, useEffect, useMemo, useState } from 'react'

import { apiRequest } from '../../api/client'
import type { Bed, Room } from '../housing/types'
import type { Contract, HousingApplication } from './types'

type ActionType = 'reject' | 'assign' | 'transfer' | 'terminate'
interface ActiveAction { type: ActionType; id: string }

const applicationColor = { Submitted: 'gold', Approved: 'green', Rejected: 'red' }

export default function ApplicationManagementPage() {
  const [applications, setApplications] = useState<HousingApplication[]>([])
  const [contracts, setContracts] = useState<Contract[]>([])
  const [beds, setBeds] = useState<Bed[]>([])
  const [rooms, setRooms] = useState<Room[]>([])
  const [filter, setFilter] = useState<string>()
  const [activeAction, setActiveAction] = useState<ActiveAction>()
  const [loading, setLoading] = useState(true)
  const [form] = Form.useForm()

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [applicationData, contractData, bedData, roomData] = await Promise.all([
        apiRequest<HousingApplication[]>('/housing-applications'),
        apiRequest<Contract[]>('/contracts'),
        apiRequest<Bed[]>('/beds'),
        apiRequest<Room[]>('/rooms'),
      ])
      setApplications(applicationData)
      setContracts(contractData)
      setBeds(bedData)
      setRooms(roomData)
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không tải được dữ liệu')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void load() }, [load])

  const availableBeds = useMemo(
    () => beds.filter((bed) => bed.status === 'Available' && bed.is_active),
    [beds],
  )
  const filteredApplications = filter
    ? applications.filter((item) => item.status === filter)
    : applications

  const openAction = (action: ActiveAction) => {
    form.resetFields()
    setActiveAction(action)
  }

  const approve = async (id: string) => {
    try {
      await apiRequest(`/housing-applications/${id}/approve`, { method: 'POST' })
      message.success('Đã duyệt đăng ký')
      await load()
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không thể duyệt')
    }
  }

  const submitAction = async (values: Record<string, string>) => {
    if (!activeAction) return
    const { type, id } = activeAction
    const path = type === 'reject'
      ? `/housing-applications/${id}/reject`
      : type === 'assign'
        ? `/contracts/${id}/assign-bed`
        : `/contracts/${id}/${type}`
    try {
      await apiRequest(path, { method: 'POST', body: JSON.stringify(values) })
      message.success(type === 'reject' ? 'Đã từ chối đăng ký' : 'Đã cập nhật hợp đồng')
      setActiveAction(undefined)
      await load()
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Thao tác không thành công')
    }
  }

  const bedOptions = availableBeds.map((bed) => {
    const room = rooms.find((item) => item.id === bed.room_id)
    return {
      value: bed.id,
      label: room ? `${room.building_code}-${room.code} / ${bed.code}` : bed.code,
    }
  })

  const actionTitle = activeAction && {
    reject: 'Từ chối đăng ký',
    assign: 'Phân giường và tạo hợp đồng',
    transfer: 'Chuyển giường',
    terminate: 'Chấm dứt hợp đồng',
  }[activeAction.type]

  return <div>
    <Typography.Title level={2}>Đăng ký và hợp đồng</Typography.Title>
    <Card title="Đăng ký ở ký túc xá" style={{ marginBottom: 16 }} extra={
      <Select allowClear placeholder="Tất cả trạng thái" style={{ width: 180 }} value={filter} onChange={setFilter}
        options={[
          { value: 'Submitted', label: 'Chờ duyệt' },
          { value: 'Approved', label: 'Đã duyệt' },
          { value: 'Rejected', label: 'Từ chối' },
        ]} />
    }>
      <Table rowKey="id" loading={loading} dataSource={filteredApplications} columns={[
        { title: 'Sinh viên', dataIndex: 'student_name' },
        { title: 'Học kỳ', dataIndex: 'term_code' },
        { title: 'Loại phòng', dataIndex: 'preferred_room_type_name' },
        { title: 'Trạng thái', dataIndex: 'status', render: (value: keyof typeof applicationColor) => <Tag color={applicationColor[value]}>{value}</Tag> },
        { title: 'Lý do', dataIndex: 'rejection_reason', render: (value) => value ?? '—' },
        {
          title: 'Thao tác',
          render: (_, item) => <Space wrap>
            {item.status === 'Submitted' && <>
              <Button type="primary" onClick={() => approve(item.id)}>Duyệt</Button>
              <Button danger onClick={() => openAction({ type: 'reject', id: item.id })}>Từ chối</Button>
            </>}
            {item.status === 'Approved' && !contracts.some((contract) => contract.application_id === item.id) &&
              <Button type="primary" onClick={() => openAction({ type: 'assign', id: item.id })}>Phân giường</Button>}
          </Space>,
        },
      ]} />
    </Card>

    <Card title="Hợp đồng">
      <Table rowKey="id" loading={loading} dataSource={contracts} columns={[
        { title: 'Số hợp đồng', dataIndex: 'contract_no' },
        { title: 'Sinh viên', dataIndex: 'student_name' },
        { title: 'Thời hạn', render: (_, item) => `${item.start_date} — ${item.end_date}` },
        { title: 'Giường hiện tại', render: (_, item) => item.current_assignment
          ? `${item.current_assignment.building_code}-${item.current_assignment.room_code} / ${item.current_assignment.bed_code}`
          : '—' },
        { title: 'Trạng thái', dataIndex: 'status', render: (value) => <Tag color={value === 'Active' ? 'green' : 'default'}>{value}</Tag> },
        {
          title: 'Thao tác',
          render: (_, item) => item.status === 'Active' && <Space>
            <Button onClick={() => openAction({ type: 'transfer', id: item.id })}>Chuyển giường</Button>
            <Button danger onClick={() => openAction({ type: 'terminate', id: item.id })}>Chấm dứt</Button>
          </Space>,
        },
      ]} />
    </Card>

    <Modal title={actionTitle} open={Boolean(activeAction)} onCancel={() => setActiveAction(undefined)}
      okText="Xác nhận" cancelText="Hủy" onOk={() => form.submit()} destroyOnHidden>
      <Form form={form} layout="vertical" onFinish={submitAction}>
        {activeAction?.type === 'reject' && <Form.Item name="reason" label="Lý do từ chối" rules={[{ required: true }]}>
          <Input.TextArea rows={3} />
        </Form.Item>}
        {activeAction?.type === 'assign' && <>
          <Form.Item name="bed_id" label="Giường" rules={[{ required: true }]}><Select options={bedOptions} /></Form.Item>
          <Form.Item name="start_date" label="Ngày bắt đầu" rules={[{ required: true }]}><Input type="date" /></Form.Item>
          <Form.Item name="end_date" label="Ngày kết thúc" rules={[{ required: true }]}><Input type="date" /></Form.Item>
        </>}
        {activeAction?.type === 'transfer' && <>
          <Form.Item name="bed_id" label="Giường mới" rules={[{ required: true }]}><Select options={bedOptions} /></Form.Item>
          <Form.Item name="transfer_date" label="Ngày chuyển" rules={[{ required: true }]}><Input type="date" /></Form.Item>
        </>}
        {activeAction?.type === 'terminate' &&
          <Form.Item name="termination_date" label="Ngày chấm dứt" rules={[{ required: true }]}><Input type="date" /></Form.Item>}
      </Form>
    </Modal>
  </div>
}
