import { DeleteOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons'
import { Button, Card, Form, Input, InputNumber, Modal, Popconfirm, Select, Space, Switch, Table, Tabs, Typography, message } from 'antd'
import { useCallback, useEffect, useState } from 'react'

import { apiRequest } from '../../api/client'
import type { Bed, Building, Room, RoomType } from './types'

type EditState =
  | { kind: 'building'; item: Building }
  | { kind: 'room-type'; item: RoomType }
  | { kind: 'room'; item: Room }
  | { kind: 'bed'; item: Bed }

export default function HousingPage() {
  const [buildings, setBuildings] = useState<Building[]>([])
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([])
  const [rooms, setRooms] = useState<Room[]>([])
  const [beds, setBeds] = useState<Bed[]>([])
  const [loading, setLoading] = useState(true)
  const [editState, setEditState] = useState<EditState>()
  const [editForm] = Form.useForm()

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [buildingData, typeData, roomData, bedData] = await Promise.all([
        apiRequest<Building[]>('/buildings'), apiRequest<RoomType[]>('/room-types'),
        apiRequest<Room[]>('/rooms'), apiRequest<Bed[]>('/beds'),
      ])
      setBuildings(buildingData); setRoomTypes(typeData); setRooms(roomData); setBeds(bedData)
    } catch (error) { message.error(error instanceof Error ? error.message : 'Không tải được dữ liệu') }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { void load() }, [load])

  const create = async (path: string, values: object) => {
    try { await apiRequest(path, { method: 'POST', body: JSON.stringify(values) }); message.success('Đã tạo dữ liệu'); await load() }
    catch (error) { message.error(error instanceof Error ? error.message : 'Không thể tạo dữ liệu') }
  }
  const remove = async (path: string) => {
    try { await apiRequest(path, { method: 'DELETE' }); message.success('Đã xóa'); await load() }
    catch (error) { message.error(error instanceof Error ? error.message : 'Không thể xóa') }
  }
  const openEdit = (state: EditState) => {
    setEditState(state)
    editForm.setFieldsValue(state.item)
  }
  const update = async (values: object) => {
    if (!editState) return
    const path = {
      building: '/buildings',
      'room-type': '/room-types',
      room: '/rooms',
      bed: '/beds',
    }[editState.kind]
    try {
      await apiRequest(`${path}/${editState.item.id}`, {
        method: 'PUT',
        body: JSON.stringify(values),
      })
      message.success('Đã cập nhật dữ liệu')
      setEditState(undefined)
      await load()
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không thể cập nhật dữ liệu')
    }
  }

  const buildingTab = <Space direction="vertical" size={16} style={{ width: '100%' }}>
    <Card title="Thêm tòa nhà"><Form layout="inline" onFinish={(v) => create('/buildings', v)} initialValues={{ floors: 5, is_active: true }}>
      <Form.Item name="code" rules={[{ required: true }]}><Input placeholder="Mã tòa" /></Form.Item>
      <Form.Item name="name" rules={[{ required: true }]}><Input placeholder="Tên tòa" /></Form.Item>
      <Form.Item name="address"><Input placeholder="Địa chỉ" /></Form.Item>
      <Form.Item name="floors" rules={[{ required: true }]}><InputNumber min={1} placeholder="Số tầng" /></Form.Item>
      <Form.Item name="is_active" valuePropName="checked"><Switch checkedChildren="Hoạt động" /></Form.Item>
      <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>Thêm</Button>
    </Form></Card>
    <Table rowKey="id" loading={loading} dataSource={buildings} columns={[
      { title: 'Mã', dataIndex: 'code' }, { title: 'Tên tòa', dataIndex: 'name' }, { title: 'Địa chỉ', dataIndex: 'address' }, { title: 'Số tầng', dataIndex: 'floors' },
      { title: '', render: (_, x) => <Space><Button icon={<EditOutlined />} onClick={() => openEdit({ kind: 'building', item: x })} /><Popconfirm title="Xóa tòa nhà?" onConfirm={() => remove(`/buildings/${x.id}`)}><Button danger icon={<DeleteOutlined />} /></Popconfirm></Space> },
    ]} />
  </Space>

  const roomTypeTab = <Space direction="vertical" size={16} style={{ width: '100%' }}>
    <Card title="Thêm loại phòng"><Form layout="inline" onFinish={(v) => create('/room-types', v)} initialValues={{ is_active: true }}>
      <Form.Item name="name" rules={[{ required: true }]}><Input placeholder="Tên loại phòng" /></Form.Item>
      <Form.Item name="default_monthly_rate" rules={[{ required: true }]}><InputNumber min={0} step={50000} placeholder="Giá/tháng" /></Form.Item>
      <Form.Item name="is_active" valuePropName="checked"><Switch checkedChildren="Hoạt động" /></Form.Item>
      <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>Thêm</Button>
    </Form></Card>
    <Table rowKey="id" loading={loading} dataSource={roomTypes} columns={[
      { title: 'Tên loại phòng', dataIndex: 'name' }, { title: 'Giá mặc định', dataIndex: 'default_monthly_rate', render: (v) => `${Number(v).toLocaleString('vi-VN')} đ` },
      { title: '', render: (_, x) => <Space><Button icon={<EditOutlined />} onClick={() => openEdit({ kind: 'room-type', item: x })} /><Popconfirm title="Xóa loại phòng?" onConfirm={() => remove(`/room-types/${x.id}`)}><Button danger icon={<DeleteOutlined />} /></Popconfirm></Space> },
    ]} />
  </Space>

  const roomTab = <Space direction="vertical" size={16} style={{ width: '100%' }}>
    <Card title="Thêm phòng"><Form layout="inline" onFinish={(v) => create('/rooms', v)} initialValues={{ floor: 1, is_active: true }}>
      <Form.Item name="building_id" rules={[{ required: true }]}><Select placeholder="Tòa nhà" style={{ width: 160 }} options={buildings.map(x => ({ value: x.id, label: `${x.code} - ${x.name}` }))} /></Form.Item>
      <Form.Item name="room_type_id" rules={[{ required: true }]}><Select placeholder="Loại phòng" style={{ width: 180 }} options={roomTypes.map(x => ({ value: x.id, label: x.name }))} /></Form.Item>
      <Form.Item name="code" rules={[{ required: true }]}><Input placeholder="Mã phòng" /></Form.Item>
      <Form.Item name="floor" rules={[{ required: true }]}><InputNumber min={1} placeholder="Tầng" /></Form.Item>
      <Form.Item name="is_active" valuePropName="checked"><Switch checkedChildren="Hoạt động" /></Form.Item>
      <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>Thêm</Button>
    </Form></Card>
    <Table rowKey="id" loading={loading} dataSource={rooms} columns={[
      { title: 'Tòa', dataIndex: 'building_code' }, { title: 'Phòng', dataIndex: 'code' }, { title: 'Tầng', dataIndex: 'floor' }, { title: 'Loại phòng', dataIndex: 'room_type_name' },
      { title: '', render: (_, x) => <Space><Button icon={<EditOutlined />} onClick={() => openEdit({ kind: 'room', item: x })} /><Popconfirm title="Xóa phòng?" onConfirm={() => remove(`/rooms/${x.id}`)}><Button danger icon={<DeleteOutlined />} /></Popconfirm></Space> },
    ]} />
  </Space>

  const bedTab = <Space direction="vertical" size={16} style={{ width: '100%' }}>
    <Card title="Thêm giường"><Form layout="inline" onFinish={(v) => create('/beds', v)} initialValues={{ is_active: true }}>
      <Form.Item name="room_id" rules={[{ required: true }]}><Select placeholder="Phòng" style={{ width: 180 }} options={rooms.map(x => ({ value: x.id, label: `${x.building_code}-${x.code}` }))} /></Form.Item>
      <Form.Item name="code" rules={[{ required: true }]}><Input placeholder="Mã giường" /></Form.Item>
      <Form.Item name="is_active" valuePropName="checked"><Switch checkedChildren="Sẵn sàng" /></Form.Item>
      <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>Thêm</Button>
    </Form></Card>
    <Table rowKey="id" loading={loading} dataSource={beds} columns={[
      { title: 'Phòng', dataIndex: 'room_id', render: (id) => rooms.find(x => x.id === id)?.code ?? id }, { title: 'Giường', dataIndex: 'code' }, { title: 'Trạng thái', dataIndex: 'status' },
      { title: '', render: (_, x) => <Space><Button icon={<EditOutlined />} onClick={() => openEdit({ kind: 'bed', item: x })} /><Popconfirm title="Xóa giường?" onConfirm={() => remove(`/beds/${x.id}`)}><Button danger icon={<DeleteOutlined />} /></Popconfirm></Space> },
    ]} />
  </Space>

  return <div><Typography.Title level={2}>Danh mục cơ sở vật chất</Typography.Title><Typography.Paragraph type="secondary">F01–F04: quản lý tòa nhà, loại phòng, phòng và giường.</Typography.Paragraph>
    <Tabs items={[{ key: 'buildings', label: `Tòa nhà (${buildings.length})`, children: buildingTab }, { key: 'types', label: `Loại phòng (${roomTypes.length})`, children: roomTypeTab }, { key: 'rooms', label: `Phòng (${rooms.length})`, children: roomTab }, { key: 'beds', label: `Giường (${beds.length})`, children: bedTab }]} />
    <Modal title="Cập nhật dữ liệu" open={Boolean(editState)} onCancel={() => setEditState(undefined)}
      okText="Lưu" cancelText="Hủy" onOk={() => editForm.submit()} destroyOnHidden>
      <Form form={editForm} layout="vertical" onFinish={update}>
        {editState?.kind === 'building' && <>
          <Form.Item name="code" label="Mã tòa" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="name" label="Tên tòa" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="address" label="Địa chỉ"><Input /></Form.Item>
          <Form.Item name="floors" label="Số tầng" rules={[{ required: true }]}><InputNumber min={1} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="is_active" label="Hoạt động" valuePropName="checked"><Switch /></Form.Item>
        </>}
        {editState?.kind === 'room-type' && <>
          <Form.Item name="name" label="Tên loại phòng" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="default_monthly_rate" label="Giá/tháng" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="is_active" label="Hoạt động" valuePropName="checked"><Switch /></Form.Item>
        </>}
        {editState?.kind === 'room' && <>
          <Form.Item name="building_id" label="Tòa nhà" rules={[{ required: true }]}><Select options={buildings.map(x => ({ value: x.id, label: x.code }))} /></Form.Item>
          <Form.Item name="room_type_id" label="Loại phòng" rules={[{ required: true }]}><Select options={roomTypes.map(x => ({ value: x.id, label: x.name }))} /></Form.Item>
          <Form.Item name="code" label="Mã phòng" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="floor" label="Tầng" rules={[{ required: true }]}><InputNumber min={1} style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="is_active" label="Hoạt động" valuePropName="checked"><Switch /></Form.Item>
        </>}
        {editState?.kind === 'bed' && <>
          <Form.Item name="room_id" label="Phòng" rules={[{ required: true }]}><Select options={rooms.map(x => ({ value: x.id, label: `${x.building_code}-${x.code}` }))} /></Form.Item>
          <Form.Item name="code" label="Mã giường" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="is_active" label="Sẵn sàng" valuePropName="checked"><Switch /></Form.Item>
        </>}
      </Form>
    </Modal>
  </div>
}
