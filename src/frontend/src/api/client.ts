import { clearSession, getAccessToken } from '../auth/session'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

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
  if (!(init.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers })
  if (response.status === 401) clearSession()
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const detail = body.detail ?? body
    const message = typeof detail === 'string'
      ? detail
      : detail.message ?? body.message ?? 'Yêu cầu không thành công.'
    throw new ApiError(message, response.status, body.errorCode ?? detail.errorCode)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export async function apiDownload(path: string): Promise<Blob> {
  const token = getAccessToken()
  const headers = new Headers()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const response = await fetch(`${apiBaseUrl}${path}`, { headers })
  if (response.status === 401) clearSession()
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new ApiError(body.detail ?? body.message ?? 'Không thể tải tệp.', response.status, body.errorCode)
  }
  return response.blob()
}
