import { Button, DatePicker, Form, Input, Typography, message } from 'antd'
import dayjs from 'dayjs'
import { useEffect } from 'react'

import { apiRequest } from '../../api/client'
import type { StudentProfile } from './types'

export default function StudentProfilePage() {
  const [form] = Form.useForm()
  useEffect(() => { void apiRequest<StudentProfile>('/student-profile/me').then(profile => form.setFieldsValue({ ...profile, date_of_birth: profile.date_of_birth ? dayjs(profile.date_of_birth) : undefined })).catch(error => message.error(error.message)) }, [form])
  const save = async (values: Record<string, unknown>) => {
    try {
      await apiRequest('/student-profile/me', { method: 'PUT', body: JSON.stringify({ ...values, date_of_birth: values.date_of_birth ? (values.date_of_birth as dayjs.Dayjs).format('YYYY-MM-DD') : null }) })
      message.success('Đã cập nhật hồ sơ')
    } catch (error) { message.error(error instanceof Error ? error.message : 'Không cập nhật được hồ sơ') }
  }
  return <div><Typography.Title level={2}>Hồ sơ sinh viên</Typography.Title><Typography.Paragraph type="secondary">Thông tin này được dùng cho đăng ký, hợp đồng và liên hệ khẩn cấp.</Typography.Paragraph>
    <Form form={form} layout="vertical" onFinish={save} style={{ maxWidth: 720 }}>
      <Form.Item name="student_code" label="Mã sinh viên" rules={[{ required: true }]}><Input /></Form.Item>
      <Form.Item name="faculty" label="Khoa"><Input /></Form.Item><Form.Item name="cohort" label="Khóa"><Input /></Form.Item>
      <Form.Item name="date_of_birth" label="Ngày sinh"><DatePicker format="DD/MM/YYYY" /></Form.Item><Form.Item name="phone" label="Số điện thoại"><Input /></Form.Item>
      <Form.Item name="address" label="Địa chỉ"><Input.TextArea /></Form.Item><Form.Item name="emergency_contact_name" label="Người liên hệ khẩn cấp"><Input /></Form.Item>
      <Form.Item name="emergency_contact_phone" label="SĐT liên hệ khẩn cấp"><Input /></Form.Item><Button type="primary" htmlType="submit">Lưu hồ sơ</Button>
    </Form>
  </div>
}
