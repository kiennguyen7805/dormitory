import type { PropsWithChildren } from 'react'
import { Navigate, useLocation } from 'react-router-dom'

import { useAuth } from './AuthContext'
import type { Role } from './types'

export function ProtectedRoute({ children, roles }: PropsWithChildren<{ roles?: Role[] }>) {
  const { user } = useAuth()
  const location = useLocation()

  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />
  if (roles && !roles.includes(user.role)) return <Navigate to={user.role === 'Student' ? '/student' : '/admin/housing'} replace />
  return children
}
