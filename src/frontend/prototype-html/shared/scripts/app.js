/* =========================================================
   APP.JS — tiện ích UI dùng chung: modal, tab, toast, format
   ========================================================= */

function fmtMoney(n) {
  return n.toLocaleString('vi-VN') + ' đ';
}
function fmtDate(d) {
  const dt = (d instanceof Date) ? d : new Date(d);
  return dt.toLocaleDateString('vi-VN');
}

/* ---------- Modal ---------- */
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('open');
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('open');
}
document.addEventListener('click', (e) => {
  if (e.target.classList && e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
  }
});

/* ---------- Tabs ----------
   Cấu trúc:
   <div class="tabs" data-tabgroup="g1">
     <div class="tab-item active" data-tab="a">A</div>
     <div class="tab-item" data-tab="b">B</div>
   </div>
   <div class="tab-panel active" data-tabpanel="a" data-tabgroup="g1">...</div>
   <div class="tab-panel" data-tabpanel="b" data-tabgroup="g1">...</div>
------------------------------------------------------------*/
document.addEventListener('click', (e) => {
  const tabEl = e.target.closest('.tab-item');
  if (!tabEl) return;
  const group = tabEl.closest('.tabs').dataset.tabgroup;
  const target = tabEl.dataset.tab;

  tabEl.closest('.tabs').querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
  tabEl.classList.add('active');

  document.querySelectorAll(`.tab-panel[data-tabgroup="${group}"]`).forEach(p => {
    p.classList.toggle('active', p.dataset.tabpanel === target);
  });
});

/* ---------- Toast ---------- */
function showToast(message, type) {
  let wrap = document.querySelector('.toast-wrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.className = 'toast-wrap';
    document.body.appendChild(wrap);
  }
  const t = document.createElement('div');
  t.className = 'toast' + (type === 'error' ? ' error' : '');
  t.textContent = message;
  wrap.appendChild(t);
  setTimeout(() => t.remove(), 3200);
}

/* ---------- Badge helper ---------- */
const STATUS_MAP = {
  Paid: ['success', 'Đã thanh toán'],
  Active: ['success', 'Đang hiệu lực'],
  Approved: ['success', 'Đã duyệt'],
  Available: ['success', 'Còn trống'],
  Resolved: ['success', 'Đã xử lý'],
  Pending: ['warning', 'Chờ xử lý'],
  Submitted: ['warning', 'Chờ duyệt'],
  PartiallyPaid: ['warning', 'Trả một phần'],
  Reserved: ['warning', 'Đã giữ chỗ'],
  UnderReview: ['warning', 'Đang xem xét'],
  Overdue: ['error', 'Quá hạn'],
  Rejected: ['error', 'Từ chối'],
  Confirmed: ['error', 'Đã xác nhận'],
  Maintenance: ['error', 'Bảo trì'],
  Draft: ['info', 'Bản nháp'],
  Importing: ['info', 'Đang import'],
  Inactive: ['neutral', 'Ngừng hoạt động'],
  Cancelled: ['neutral', 'Đã huỷ'],
  Terminated: ['neutral', 'Đã chấm dứt'],
  Occupied: ['info', 'Đang ở'],
};
function badgeHtml(statusKey) {
  const [cls, label] = STATUS_MAP[statusKey] || ['neutral', statusKey];
  return `<span class="badge badge-${cls}">${label}</span>`;
}

/* ---------- AI draft simulate ---------- */
function simulateAiDraft(btn, targetId, generator) {
  const target = document.getElementById(targetId);
  const originalLabel = btn.innerHTML;
  btn.disabled = true;
  target.style.display = 'block';
  target.innerHTML = `<span class="ai-label">✨ Bản nháp AI</span><div class="ai-loading"><span class="spinner"></span> Đang soạn nội dung, vui lòng chờ...</div>`;
  setTimeout(() => {
    target.innerHTML = `<span class="ai-label">✨ Bản nháp AI</span>${generator()}`;
    btn.disabled = false;
    btn.innerHTML = originalLabel;
  }, 900);
}
