import { clearSession, getAccessToken } from '../auth/session'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly errorCode?: string,
  ) {
    super(message)
  }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getAccessToken()
  const headers = new Headers(init.headers)
  headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers })
  if (response.status === 401) clearSession()
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const detail = body.detail ?? body
    throw new ApiError(detail.message ?? 'Yêu cầu không thành công.', response.status, detail.errorCode)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}
