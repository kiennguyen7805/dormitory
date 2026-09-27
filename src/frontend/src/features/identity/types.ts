import type { Role } from '../../auth/types'

export interface ManagedUser {
  id: string
  email: string
  full_name: string
  role: Role
  is_active: boolean
  permissions: string[]
}

export interface StudentProfile {
  user_id: string
  email: string
  full_name: string
  student_code: string
  faculty: string
  cohort: string
  date_of_birth?: string
  phone: string
  address: string
  emergency_contact_name: string
  emergency_contact_phone: string
}

export interface LoginEvent {
  id: string
  email: string
  succeeded: boolean
  ip_address: string
  user_agent: string
  occurred_at: string
}

export interface AuditLog {
  id: string
  action: string
  entity_type: string
  entity_id: string
  created_at: string
}
