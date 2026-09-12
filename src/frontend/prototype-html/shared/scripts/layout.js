/* =========================================================
   LAYOUT — sinh sidebar + topbar dùng chung cho mọi trang.
   body cần data-page="..." ; data-role="admin|staff|student"
   ========================================================= */
(function () {
  const ICONS = {
    dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>',
    housing: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-6h6v6"/></svg>',
    applications: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12h6M9 16h6M9 8h6"/><rect x="4" y="3" width="16" height="18" rx="2"/></svg>',
    contracts: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3v5h5"/><path d="M6 3h8l5 5v13H6z"/><path d="M9 13.5l2 2 4-4.5"/></svg>',
    utilities: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>',
    billing: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/><path d="M7 15h4"/></svg>',
    violations: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 2.7 18a1.5 1.5 0 0 0 1.3 2.2h16a1.5 1.5 0 0 0 1.3-2.2L13.7 3.9a1.5 1.5 0 0 0-2.6 0Z"/></svg>',
    reports: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/></svg>',
    ai: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3M12 18v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M3 12h3M18 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/><circle cx="12" cy="12" r="3.2"/></svg>',
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-6h6v6"/></svg>',
    register: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>',
    logout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/></svg>',
    bell: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>'
  };

  const NAV = {
    admin: [
      { group: 'Tổng quan', items: [
        { key: 'dashboard', label: 'Dashboard', href: '../dashboard/admin-dashboard.html', icon: 'dashboard' },
      ]},
      { group: 'Vận hành', items: [
        { key: 'room-matrix', label: 'Tòa / Phòng / Giường', href: '../housing/room-matrix.html', icon: 'housing' },
        { key: 'applications', label: 'Đăng ký ở KTX', href: '../applications/application-management.html', icon: 'applications' },
        { key: 'contracts', label: 'Hợp đồng', href: '../contracts/contract-management.html', icon: 'contracts' },
        { key: 'utilities', label: 'Điện nước', href: '../utilities/utility-management.html', icon: 'utilities' },
        { key: 'billing', label: 'Hoá đơn & Thu phí', href: '../billing/billing-management.html', icon: 'billing' },
        { key: 'violations', label: 'Kỷ luật', href: '../violations/violation-management.html', icon: 'violations' },
      ]},
      { group: 'Trợ lý AI', items: [
        { key: 'ai', label: 'Trợ lý AI', href: '../ai/ai-assistant.html', icon: 'ai' },
      ]},
    ],
    staff: null, // dùng chung menu admin, chỉ khác quyền (staff không thấy 1 vài mục — xử lý ở data-hide-for-staff)
    student: [
      { group: 'Của tôi', items: [
        { key: 'dashboard', label: 'Chỗ ở hiện tại', href: '../dashboard/student-dashboard.html', icon: 'home' },
        { key: 'bills', label: 'Hoá đơn của tôi', href: '../billing/student-bills.html', icon: 'billing' },
        { key: 'violations', label: 'Vi phạm của tôi', href: '../violations/student-violations.html', icon: 'violations' },
        { key: 'register', label: 'Đăng ký / Chuyển phòng', href: '../applications/student-application.html', icon: 'register' },
      ]},
    ],
  };

  const ROLE_LABEL = { admin: 'Quản trị viên', staff: 'Cán bộ KTX', student: 'Sinh viên' };
  const ROLE_NAME  = { admin: 'Nguyễn Văn Admin', staff: 'Trần Thị Cán Bộ', student: 'Lê Văn Sinh Viên' };
  const ROLE_INITIAL = { admin: 'AD', staff: 'CB', student: 'SV' };

  function initials(name) {
    return name.split(' ').slice(-2).map(w => w[0]).join('').toUpperCase();
  }

  function renderLayout() {
    const body = document.body;
    const role = body.dataset.role || 'admin';
    const page = body.dataset.page || '';
    const title = body.dataset.title || '';
    const navGroups = NAV[role] || NAV.admin;
    const isStaff = role === 'staff';

    let navHtml = '';
    navGroups.forEach(g => {
      navHtml += `<div class="sidebar-group-label">${g.group}</div>`;
      g.items.forEach(it => {
        if (isStaff && it.hideForStaff) return;
        const active = it.key === page ? 'active' : '';
        navHtml += `<a class="nav-item ${active}" href="${it.href}">${ICONS[it.icon] || ''}<span>${it.label}</span></a>`;
      });
    });

    const roleLabel = isStaff ? 'Cán bộ KTX' : ROLE_LABEL[role];
    const userName = isStaff ? ROLE_NAME.staff : ROLE_NAME[role];

    const shell = document.createElement('div');
    shell.className = 'app-shell';
    shell.innerHTML = `
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-brand">
          <div class="sidebar-brand-mark">KTX</div>
          <div class="sidebar-brand-text">Dormitory<small>Hệ thống quản lý KTX</small></div>
        </div>
        <nav class="sidebar-nav">${navHtml}</nav>
        <div class="sidebar-footer">
          <a class="logout-link" href="../../../index.html">${ICONS.logout}<span>Đăng xuất</span></a>
        </div>
      </aside>
      <div class="main-area">
        <header class="topbar">
          <div class="topbar-left">
            <button class="icon-btn" id="sidebarToggle" aria-label="Mở menu">${ICONS.menu}</button>
            <div class="topbar-title">${title}</div>
          </div>
          <div class="topbar-right">
            <button class="icon-btn" aria-label="Thông báo">${ICONS.bell}<span class="dot"></span></button>
            <div class="user-chip">
              <div class="avatar">${initials(userName)}</div>
              <div>
                <div class="user-chip-name">${userName}</div>
                <div class="user-chip-role">${roleLabel}</div>
              </div>
            </div>
          </div>
        </header>
        <main class="content" id="pageContent"></main>
      </div>
    `;

    // Move any existing body content (the page's own markup) into #pageContent
    const existing = Array.from(body.childNodes);
    body.innerHTML = '';
    body.appendChild(shell);
    const contentEl = shell.querySelector('#pageContent');
    existing.forEach(node => contentEl.appendChild(node));

    shell.querySelector('#sidebarToggle').addEventListener('click', () => {
      shell.querySelector('#sidebar').classList.toggle('open');
    });
  }

  document.addEventListener('DOMContentLoaded', renderLayout);
})();
