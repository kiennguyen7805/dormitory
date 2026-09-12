/**
 * Dormitory API Client - Kết nối Frontend với Backend Python (FastAPI)
 * Mặc định kết nối tới http://127.0.0.1:8000/api
 * Nếu Backend chưa bật, tự động fallback về mock-data.js để không làm gián đoạn giao diện.
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiClient {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  getToken() {
    return localStorage.getItem('dormitory_token') || '';
  }

  setToken(token) {
    localStorage.setItem('dormitory_token', token);
  }

  clearToken() {
    localStorage.removeItem('dormitory_token');
    localStorage.removeItem('dormitory_user');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || `HTTP Error ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.warn(`[API Client] Endpoint ${endpoint} gọi không thành công (${err.message}). Sử dụng Mock Data fallback.`);
      return null;
    }
  }

  // Auth
  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    if (data && data.token) {
      this.setToken(data.token);
      localStorage.setItem('dormitory_user', JSON.stringify(data));
    }
    return data;
  }

  async logout() {
    await this.request('/auth/logout', { method: 'POST' });
    this.clearToken();
  }

  // Housing
  async getBuildings() {
    return await this.request('/buildings');
  }

  async getRooms(buildingId = '') {
    return await this.request(`/rooms${buildingId ? `?building_id=${buildingId}` : ''}`);
  }

  async getBeds(roomId = '') {
    return await this.request(`/beds${roomId ? `?room_id=${roomId}` : ''}`);
  }

  async getRoomMatrix(buildingId = '') {
    return await this.request(`/room-matrix${buildingId ? `?building_id=${buildingId}` : ''}`);
  }

  // Contracts & Applications
  async getApplications(status = '') {
    return await this.request(`/housing-applications${status ? `?status=${status}` : ''}`);
  }

  async createApplication(appData) {
    return await this.request('/housing-applications', {
      method: 'POST',
      body: JSON.stringify(appData)
    });
  }

  async getContracts() {
    return await this.request('/contracts');
  }

  // Utilities
  async getTariffs() {
    return await this.request('/utility-tariffs');
  }

  async getMeterReadings(roomId = '') {
    return await this.request(`/meter-readings${roomId ? `?room_id=${roomId}` : ''}`);
  }

  // Billing
  async getBills(studentId = '', status = '') {
    let query = [];
    if (studentId) query.push(`student_id=${studentId}`);
    if (status) query.push(`status=${status}`);
    const qs = query.length ? `?${query.join('&')}` : '';
    return await this.request(`/bills${qs}`);
  }

  async recordPayment(paymentData) {
    return await this.request('/payments', {
      method: 'POST',
      body: JSON.stringify(paymentData)
    });
  }

  // Violations
  async getViolations(studentId = '') {
    return await this.request(`/violations${studentId ? `?student_id=${studentId}` : ''}`);
  }

  // Reports
  async getOccupancyReport() {
    return await this.request('/reports/occupancy');
  }

  async getRevenueReport() {
    return await this.request('/reports/revenue');
  }

  // AI
  async draftPaymentReminder(studentId) {
    return await this.request('/ai/draft-payment-reminder', {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId })
    });
  }
}

// Global instance
window.apiClient = new ApiClient();
