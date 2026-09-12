/* =========================================================
   MOCK DATA — dữ liệu mẫu minh hoạ giao diện (không có backend thật)
   ========================================================= */
const MOCK = {
  buildings: [
    { code: 'A', name: 'Toà A', floors: 5, status: 'Active' },
    { code: 'B', name: 'Toà B', floors: 4, status: 'Active' },
  ],
  kpi: {
    totalBeds: 240,
    occupiedBeds: 198,
    occupancyRate: 82.5,
    debt: 46500000,
  },
  applications: [
    { id: 'DK-1024', student: 'Phạm Thị Lan', code: 'SV0231', term: 'HK1 2026-2027', roomType: 'Phòng 4 người', status: 'Submitted', date: '2026-08-20' },
    { id: 'DK-1023', student: 'Nguyễn Văn Bình', code: 'SV0198', term: 'HK1 2026-2027', roomType: 'Phòng 6 người', status: 'Submitted', date: '2026-08-19' },
    { id: 'DK-1019', student: 'Trần Minh Khoa', code: 'SV0177', term: 'HK1 2026-2027', roomType: 'Phòng 4 người', status: 'Approved', date: '2026-08-15' },
    { id: 'DK-1011', student: 'Đỗ Thu Hà', code: 'SV0142', term: 'HK1 2026-2027', roomType: 'Phòng 6 người', status: 'Rejected', date: '2026-08-10' },
  ],
  contracts: [
    { no: 'HD-0231', student: 'Trần Minh Khoa', code: 'SV0177', room: 'A-305', bed: 'A-305-02', start: '2026-08-16', end: '2027-06-30', status: 'Active', rate: 850000 },
    { no: 'HD-0229', student: 'Vũ Thị Ngọc', code: 'SV0120', room: 'A-201', bed: 'A-201-01', start: '2026-08-01', end: '2027-06-30', status: 'Active', rate: 950000 },
    { no: 'HD-0180', student: 'Lê Quang Huy', code: 'SV0088', room: 'B-102', bed: 'B-102-03', start: '2025-08-10', end: '2026-06-30', status: 'Terminated', rate: 850000 },
  ],
  bills: [
    { no: 'HD2608-0231', student: 'Trần Minh Khoa', code: 'SV0177', period: 'Tháng 08/2026', total: 1250000, paid: 0, status: 'Overdue', due: '2026-09-05' },
    { no: 'HD2608-0229', student: 'Vũ Thị Ngọc', code: 'SV0120', period: 'Tháng 08/2026', total: 1380000, paid: 700000, status: 'PartiallyPaid', due: '2026-09-05' },
    { no: 'HD2607-0198', student: 'Nguyễn Văn Bình', code: 'SV0198', period: 'Tháng 07/2026', total: 1120000, paid: 1120000, status: 'Paid', due: '2026-08-05' },
    { no: 'HD2607-0177', student: 'Trần Minh Khoa', code: 'SV0177', period: 'Tháng 07/2026', total: 1180000, paid: 1180000, status: 'Paid', due: '2026-08-05' },
  ],
  violations: [
    { id: 'VP-0087', student: 'Nguyễn Văn Bình', code: 'SV0198', type: 'Gây ồn sau 22h', severity: 'Nhẹ', status: 'Recorded', date: '2026-08-28', fine: 0 },
    { id: 'VP-0086', student: 'Trần Minh Khoa', code: 'SV0177', type: 'Nấu ăn sai quy định', severity: 'Trung bình', status: 'Confirmed', date: '2026-08-20', fine: 100000 },
    { id: 'VP-0080', student: 'Lê Quang Huy', code: 'SV0088', type: 'Vi phạm giờ giới nghiêm', severity: 'Nặng', status: 'Rejected', date: '2026-07-15', fine: 0 },
  ],
  meterReadings: [
    { room: 'A-305', period: 'Kỳ 08/2026', electricPrev: 1220, electricCur: 1340, waterPrev: 88, waterCur: 96, source: 'Manual' },
    { room: 'A-201', period: 'Kỳ 08/2026', electricPrev: 980, electricCur: 1085, waterPrev: 70, waterCur: 79, source: 'ExcelImport' },
  ],
  tariffTiers: {
    electric: [
      { from: 0, to: 50, price: 1800 },
      { from: 51, to: 100, price: 2200 },
      { from: 101, to: null, price: 2800 },
    ],
    water: [
      { from: 0, to: 10, price: 8000 },
      { from: 11, to: null, price: 12000 },
    ],
  },
  studentSelf: {
    name: 'Trần Minh Khoa',
    code: 'SV0177',
    building: 'Toà A',
    room: 'A-305',
    bed: 'A-305-02',
    contractNo: 'HD-0231',
    contractEnd: '2027-06-30',
    balanceDue: 1250000,
  },
};
