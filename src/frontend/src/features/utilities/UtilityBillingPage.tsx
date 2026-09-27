import {
  Alert,
  Button,
  Card,
  Col,
  Divider,
  Form,
  Input,
  InputNumber,
  message,
  Row,
  Select,
  Space,
  Statistic,
  Table,
  Tabs,
  Tag,
  Typography,
  Upload,
} from 'antd'
import type { UploadProps } from 'antd'
import { useCallback, useEffect, useState } from 'react'

import { apiDownload, apiRequest } from '../../api/client'
import type { Bill, ImportPreview, Meter, MeterReading, Utility, UtilityTariff } from './types'

interface Room { id: string; code: string; building_code?: string }
interface Contract { id: string; contract_no: string; student_name: string; status: string }

const money = (value: string | number) => Number(value).toLocaleString('vi-VN') + ' đ'

export default function UtilityBillingPage() {
  const [loading, setLoading] = useState(false)
  const [utilities, setUtilities] = useState<Utility[]>([])
  const [meters, setMeters] = useState<Meter[]>([])
  const [tariffs, setTariffs] = useState<UtilityTariff[]>([])
  const [readings, setReadings] = useState<MeterReading[]>([])
  const [bills, setBills] = useState<Bill[]>([])
  const [rooms, setRooms] = useState<Room[]>([])
  const [contracts, setContracts] = useState<Contract[]>([])
  const [preview, setPreview] = useState<ImportPreview>()
  const [tariffType, setTariffType] = useState('Tiered')
  const [tariffForm] = Form.useForm()
  const [meterForm] = Form.useForm()
  const [readingForm] = Form.useForm()
  const [billForm] = Form.useForm()

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [utilityData, meterData, tariffData, readingData, billData, roomData, contractData] = await Promise.all([
        apiRequest<Utility[]>('/utilities'),
        apiRequest<Meter[]>('/meters'),
        apiRequest<UtilityTariff[]>('/utility-tariffs'),
        apiRequest<MeterReading[]>('/meter-readings'),
        apiRequest<Bill[]>('/bills'),
        apiRequest<Room[]>('/rooms'),
        apiRequest<Contract[]>('/contracts'),
      ])
      setUtilities(utilityData)
      setMeters(meterData)
      setTariffs(tariffData)
      setReadings(readingData)
      setBills(billData)
      setRooms(roomData)
      setContracts(contractData)
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Không tải được dữ liệu tuần 3.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void loadData() }, [loadData])

  const createTariff = async (values: Record<string, string | number>) => {
    const tiered = values.calculation_type === 'Tiered'
    await apiRequest('/utility-tariffs', {
      method: 'POST',
      body: JSON.stringify({
        utility_id: values.utility_id,
        name: values.name,
        effective_from: values.effective_from,
        effective_to: values.effective_to || null,
        calculation_type: values.calculation_type,
        tiers: tiered
          ? [
            { tier_order: 1, from_quantity: 0, to_quantity: values.first_limit, unit_price: values.first_price },
            { tier_order: 2, from_quantity: values.first_limit, to_quantity: null, unit_price: values.next_price },
          ]
          : [{ tier_order: 1, from_quantity: 0, to_quantity: null, unit_price: values.first_price }],
      }),
    })
    message.success('Đã tạo biểu giá và lưu các bậc giá.')
    tariffForm.resetFields()
    await loadData()
  }

  const createMeter = async (values: Record<string, string | number>) => {
    await apiRequest('/meters', { method: 'POST', body: JSON.stringify(values) })
    message.success('Đã thêm công tơ cho phòng.')
    meterForm.resetFields()
    await loadData()
  }

  const createReading = async (values: Record<string, string | number>) => {
    await apiRequest('/meter-readings', { method: 'POST', body: JSON.stringify(values) })
    message.success('Đã ghi chỉ số và tính tiền theo biểu giá hiệu lực.')
    readingForm.resetFields()
    await loadData()
  }

  const downloadTemplate = async () => {
    const blob = await apiDownload('/meter-readings/template')
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'meter-readings-template.xlsx'
    anchor.click()
    URL.revokeObjectURL(url)
  }

  const previewExcel: NonNullable<UploadProps['customRequest']> = async (options) => {
    try {
      const formData = new FormData()
      formData.append('file', options.file as Blob)
      const result = await apiRequest<ImportPreview>('/meter-readings/import/preview', {
        method: 'POST',
        body: formData,
      })
      setPreview(result)
      options.onSuccess?.(result)
      message.success(`Đã đọc ${result.total_rows} dòng từ Excel.`)
    } catch (error) {
      options.onError?.(error as Error)
      message.error(error instanceof Error ? error.message : 'Không đọc được tệp Excel.')
    }
  }

  const confirmImport = async () => {
    if (!preview) return
    await apiRequest(`/meter-readings/import/${preview.batch_id}/confirm`, { method: 'POST' })
    message.success(`Đã nhập ${preview.valid_rows} chỉ số từ Excel.`)
    setPreview(undefined)
    await loadData()
  }

  const generateBill = async (values: Record<string, string>) => {
    const result = await apiRequest<Bill>('/bills/generate', {
      method: 'POST',
      body: JSON.stringify({
        ...values,
        idempotency_key: `${values.contract_id}-${values.period_start}-${values.period_end}`,
      }),
    })
    message.success(`Đã sinh hóa đơn ${result.bill_no}. Gửi lại cùng kỳ sẽ không tạo trùng.`)
    billForm.resetFields()
    await loadData()
  }

  const overview = <>
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}><Card><Statistic title="Loại dịch vụ" value={utilities.length} /></Card></Col>
      <Col xs={24} sm={12} lg={6}><Card><Statistic title="Công tơ" value={meters.length} /></Card></Col>
      <Col xs={24} sm={12} lg={6}><Card><Statistic title="Lượt ghi chỉ số" value={readings.length} /></Card></Col>
      <Col xs={24} sm={12} lg={6}><Card><Statistic title="Hóa đơn" value={bills.length} /></Card></Col>
    </Row>
    <Divider />
    <Row gutter={[16, 16]}>
      <Col xs={24} xl={12}>
        <Card title="Tạo biểu giá">
          <Form form={tariffForm} layout="vertical" onFinish={createTariff} initialValues={{ calculation_type: 'Tiered' }}>
            <Row gutter={12}>
              <Col span={12}><Form.Item name="utility_id" label="Dịch vụ" rules={[{ required: true }]}><Select options={utilities.map(x => ({ value: x.id, label: `${x.name} (${x.unit})` }))} /></Form.Item></Col>
              <Col span={12}><Form.Item name="name" label="Tên biểu giá" rules={[{ required: true }]}><Input /></Form.Item></Col>
              <Col span={8}><Form.Item name="effective_from" label="Hiệu lực từ" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
              <Col span={8}><Form.Item name="effective_to" label="Hiệu lực đến"><Input type="date" /></Form.Item></Col>
              <Col span={8}><Form.Item name="calculation_type" label="Cách tính"><Select onChange={setTariffType} options={[{ value: 'Tiered', label: 'Lũy tiến' }, { value: 'Flat', label: 'Đồng giá' }]} /></Form.Item></Col>
              {tariffType === 'Tiered' && <Col span={8}><Form.Item name="first_limit" label="Mức bậc 1" rules={[{ required: true }]}><InputNumber min={0.001} style={{ width: '100%' }} /></Form.Item></Col>}
              <Col span={8}><Form.Item name="first_price" label="Đơn giá bậc 1" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item></Col>
              {tariffType === 'Tiered' && <Col span={8}><Form.Item name="next_price" label="Đơn giá bậc 2+" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item></Col>}
            </Row>
            <Button type="primary" htmlType="submit">Lưu biểu giá</Button>
          </Form>
        </Card>
      </Col>
      <Col xs={24} xl={12}>
        <Card title="Gắn công tơ vào phòng">
          <Form form={meterForm} layout="vertical" onFinish={createMeter} initialValues={{ initial_reading: 0 }}>
            <Row gutter={12}>
              <Col span={12}><Form.Item name="utility_id" label="Dịch vụ" rules={[{ required: true }]}><Select options={utilities.map(x => ({ value: x.id, label: x.name }))} /></Form.Item></Col>
              <Col span={12}><Form.Item name="room_id" label="Phòng" rules={[{ required: true }]}><Select showSearch options={rooms.map(x => ({ value: x.id, label: `${x.building_code ?? ''}-${x.code}` }))} /></Form.Item></Col>
              <Col span={12}><Form.Item name="meter_code" label="Mã công tơ" rules={[{ required: true }]}><Input /></Form.Item></Col>
              <Col span={12}><Form.Item name="initial_reading" label="Chỉ số ban đầu" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item></Col>
            </Row>
            <Button type="primary" htmlType="submit">Thêm công tơ</Button>
          </Form>
        </Card>
      </Col>
    </Row>
    <Divider />
    <Table rowKey="id" loading={loading} dataSource={tariffs} pagination={{ pageSize: 6 }} columns={[
      { title: 'Dịch vụ', dataIndex: 'utility_name' },
      { title: 'Biểu giá', dataIndex: 'name' },
      { title: 'Từ ngày', dataIndex: 'effective_from' },
      { title: 'Cách tính', dataIndex: 'calculation_type', render: value => value === 'Tiered' ? 'Lũy tiến' : 'Đồng giá' },
      { title: 'Số bậc', dataIndex: 'tiers', render: tiers => tiers.length },
    ]} />
  </>

  const metering = <>
    <Row gutter={[16, 16]}>
      <Col xs={24} lg={12}>
        <Card title="Ghi chỉ số thủ công">
          <Form form={readingForm} layout="vertical" onFinish={createReading}>
            <Form.Item name="meter_id" label="Công tơ" rules={[{ required: true }]}><Select showSearch options={meters.map(x => ({ value: x.id, label: `${x.meter_code} · ${x.room_label} · ${x.utility_name}` }))} /></Form.Item>
            <Row gutter={12}>
              <Col span={12}><Form.Item name="period_start" label="Đầu kỳ" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
              <Col span={12}><Form.Item name="period_end" label="Cuối kỳ" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
              <Col span={12}><Form.Item name="previous_reading" label="Chỉ số trước" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item></Col>
              <Col span={12}><Form.Item name="current_reading" label="Chỉ số hiện tại" rules={[{ required: true }]}><InputNumber min={0} style={{ width: '100%' }} /></Form.Item></Col>
            </Row>
            <Button type="primary" htmlType="submit">Tính và lưu chỉ số</Button>
          </Form>
        </Card>
      </Col>
      <Col xs={24} lg={12}>
        <Card title="Nhập chỉ số bằng Excel">
          <Space wrap>
            <Button onClick={downloadTemplate}>Tải file mẫu</Button>
            <Upload accept=".xlsx" maxCount={1} customRequest={previewExcel} showUploadList={false}><Button type="primary">Chọn Excel để xem trước</Button></Upload>
          </Space>
          {preview && <>
            <Alert style={{ marginTop: 16 }} type={preview.invalid_rows ? 'error' : 'success'} showIcon message={`${preview.valid_rows} dòng hợp lệ · ${preview.invalid_rows} dòng lỗi`} />
            <Table size="small" rowKey="row_number" dataSource={preview.rows} pagination={false} columns={[
              { title: 'Dòng', dataIndex: 'row_number' },
              { title: 'Công tơ', dataIndex: 'meter_code' },
              { title: 'Tiêu thụ', dataIndex: 'consumption' },
              { title: 'Kết quả', render: (_, row) => row.valid ? <Tag color="green">Hợp lệ</Tag> : <Typography.Text type="danger">{row.errors.join(', ')}</Typography.Text> },
            ]} />
            <Button type="primary" disabled={preview.invalid_rows > 0} onClick={confirmImport}>Xác nhận nhập dữ liệu</Button>
          </>}
        </Card>
      </Col>
    </Row>
    <Divider />
    <Table rowKey="id" loading={loading} dataSource={readings} columns={[
      { title: 'Công tơ', dataIndex: 'meter_code' },
      { title: 'Dịch vụ', dataIndex: 'utility_code' },
      { title: 'Kỳ', render: (_, row) => `${row.period_start} → ${row.period_end}` },
      { title: 'Chỉ số', render: (_, row) => `${row.previous_reading} → ${row.current_reading}` },
      { title: 'Tiêu thụ', dataIndex: 'consumption' },
      { title: 'Thành tiền', dataIndex: 'calculated_amount', render: money },
      { title: 'Nguồn', dataIndex: 'source' },
    ]} />
  </>

  const billing = <>
    <Card title="Sinh hóa đơn tiền phòng + điện + nước">
      <Alert style={{ marginBottom: 16 }} type="info" showIcon message="Khóa chống trùng được tạo theo hợp đồng và kỳ. Nhấn lại sẽ trả về đúng hóa đơn cũ." />
      <Form form={billForm} layout="vertical" onFinish={generateBill}>
        <Row gutter={12}>
          <Col xs={24} lg={8}><Form.Item name="contract_id" label="Hợp đồng" rules={[{ required: true }]}><Select showSearch options={contracts.filter(x => x.status === 'Active').map(x => ({ value: x.id, label: `${x.contract_no} · ${x.student_name}` }))} /></Form.Item></Col>
          <Col xs={12} lg={4}><Form.Item name="period_start" label="Đầu kỳ" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
          <Col xs={12} lg={4}><Form.Item name="period_end" label="Cuối kỳ" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
          <Col xs={12} lg={4}><Form.Item name="issued_date" label="Ngày phát hành" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
          <Col xs={12} lg={4}><Form.Item name="due_date" label="Hạn thanh toán" rules={[{ required: true }]}><Input type="date" /></Form.Item></Col>
        </Row>
        <Button type="primary" htmlType="submit">Sinh hóa đơn</Button>
      </Form>
    </Card>
    <Divider />
    <Table rowKey="id" loading={loading} dataSource={bills} expandable={{ expandedRowRender: bill => <Table rowKey="id" size="small" pagination={false} dataSource={bill.items} columns={[{ title: 'Khoản thu', dataIndex: 'description' }, { title: 'Số tiền', dataIndex: 'amount', render: money }]} /> }} columns={[
      { title: 'Số hóa đơn', dataIndex: 'bill_no' },
      { title: 'Kỳ', render: (_, row) => `${row.period_start} → ${row.period_end}` },
      { title: 'Trạng thái', dataIndex: 'status', render: value => <Tag color="blue">{value}</Tag> },
      { title: 'Tổng tiền', dataIndex: 'total_amount', render: money },
      { title: 'Còn lại', dataIndex: 'balance_amount', render: money },
    ]} />
  </>

  return <Space direction="vertical" size="large" style={{ width: '100%' }}>
    <div><Typography.Title level={2}>Điện, nước & hóa đơn</Typography.Title><Typography.Text type="secondary">Thiết lập biểu giá, nhập chỉ số, xem trước Excel và sinh hóa đơn tuần 3.</Typography.Text></div>
    <Tabs items={[{ key: 'overview', label: 'Cấu hình', children: overview }, { key: 'metering', label: 'Ghi chỉ số', children: metering }, { key: 'billing', label: 'Hóa đơn', children: billing }]} />
  </Space>
}
