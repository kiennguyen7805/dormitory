import { EditOutlined, KeyOutlined, PlusOutlined } from '@ant-design/icons'
import { Button, Form, Input, Modal, Select, Space, Switch, Table, Tag, Typography, message } from 'antd'
import { useCallback, useEffect, useState } from 'react'

import { apiRequest } from '../../api/client'
import type { ManagedUser } from './types'

export default function UserManagementPage() {
  const [users, setUsers] = useState<ManagedUser[]>([])
  const [editing, setEditing] = useState<ManagedUser>()
  const [openCreate, setOpenCreate] = useState(false)
  const [form] = Form.useForm()

  const load = useCallback(async () => {
    try { setUsers(await apiRequest<ManagedUser[]>('/users')) }
    catch (error) { message.error(error instanceof Error ? error.message : 'Không tải được tài khoản') }
  }, [])
  useEffect(() => { void load() }, [load])

  const save = async (values: Record<string, unknown>) => {
    try {
      await apiRequest(editing ? `/users/${editing.id}` : '/users', {
        method: editing ? 'PUT' : 'POST', body: JSON.stringify(values),
      })
      message.success(editing ? 'Đã cập nhật tài khoản' : 'Đã tạo tài khoản')
      setEditing(undefined); setOpenCreate(false); form.resetFields(); await load()
    } catch (error) { message.error(error instanceof Error ? error.message : 'Không lưu được tài khoản') }
  }

  const resetPassword = async (user: ManagedUser) => {
    const password = window.prompt(`Mật khẩu mới cho ${user.email} (tối thiểu 8 ký tự)`)
    if (!password) return
    try {
      await apiRequest(`/users/${user.id}/reset-password`, { method: 'POST', body: JSON.stringify({ new_password: password }) })
      message.success('Đã đặt lại mật khẩu')
    } catch (error) { message.error(error instanceof Error ? error.message : 'Không đặt lại được mật khẩu') }
  }

  return <div>
    <Space style={{ width: '100%', justifyContent: 'space-between' }}>
      <div><Typography.Title level={2}>Quản lý tài khoản</Typography.Title><Typography.Paragraph type="secondary">Tạo, phân vai trò, khóa/mở và đặt lại mật khẩu.</Typography.Paragraph></div>
      <Button type="primary" icon={<PlusOutlined />} onClick={() => { setEditing(undefined); form.resetFields(); form.setFieldsValue({ role: 'Student', is_active: true }); setOpenCreate(true) }}>Tạo tài khoản</Button>
    </Space>
    <Table rowKey="id" dataSource={users} columns={[
      { title: 'Họ tên', dataIndex: 'full_name' }, { title: 'Email', dataIndex: 'email' },
      { title: 'Vai trò', dataIndex: 'role', render: (value) => <Tag color="blue">{value}</Tag> },
      { title: 'Trạng thái', dataIndex: 'is_active', render: (value) => <Tag color={value ? 'green' : 'red'}>{value ? 'Hoạt động' : 'Đã khóa'}</Tag> },
      { title: '', render: (_, user) => <Space><Button icon={<EditOutlined />} onClick={() => { setEditing(user); form.setFieldsValue(user) }} /><Button icon={<KeyOutlined />} onClick={() => void resetPassword(user)} /></Space> },
    ]} />
    <Modal title={editing ? 'Cập nhật tài khoản' : 'Tạo tài khoản'} open={Boolean(editing) || openCreate} onCancel={() => { setEditing(undefined); setOpenCreate(false) }} onOk={() => form.submit()} okText="Lưu">
      <Form form={form} layout="vertical" onFinish={save}>
        {!editing && <><Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}><Input /></Form.Item><Form.Item name="password" label="Mật khẩu" rules={[{ required: true, min: 8 }]}><Input.Password /></Form.Item></>}
        <Form.Item name="full_name" label="Họ tên" rules={[{ required: true }]}><Input /></Form.Item>
        <Form.Item name="role" label="Vai trò" rules={[{ required: true }]}><Select options={['Admin', 'Staff', 'Student'].map(value => ({ value, label: value }))} /></Form.Item>
        {editing && <Form.Item name="is_active" label="Đang hoạt động" valuePropName="checked"><Switch /></Form.Item>}
      </Form>
    </Modal>
  </div>
}
