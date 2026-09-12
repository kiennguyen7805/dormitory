import { createContext, useContext, useMemo, useState, type PropsWithChildren } from 'react'

import { apiRequest } from '../api/client'
import { clearSession, getSession, saveSession } from './session'
import type { Session, User } from './types'

interface AuthValue {
  user: User | null
  login: (email: string, password: string) => Promise<User>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthValue | null>(null)

export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<User | null>(() => getSession()?.user ?? null)

  const value = useMemo<AuthValue>(
    () => ({
      user,
      async login(email, password) {
        const session = await apiRequest<Session>('/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        })
        saveSession(session)
        setUser(session.user)
        return session.user
      },
      async logout() {
        try {
          await apiRequest<void>('/auth/logout', { method: 'POST' })
        } finally {
          clearSession()
          setUser(null)
        }
      },
    }),
    [user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthValue {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used inside AuthProvider')
  return value
}
