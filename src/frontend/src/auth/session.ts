import type { Session } from './types'

const sessionKey = 'dormitory.session'

export function getSession(): Session | null {
  const value = localStorage.getItem(sessionKey)
  if (!value) return null
  try {
    return JSON.parse(value) as Session
  } catch {
    clearSession()
    return null
  }
}

export function saveSession(session: Session): void {
  localStorage.setItem(sessionKey, JSON.stringify(session))
}

export function clearSession(): void {
  localStorage.removeItem(sessionKey)
}

export function getAccessToken(): string | null {
  return getSession()?.access_token ?? null
}
