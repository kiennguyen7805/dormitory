export type Role = 'Admin' | 'Staff' | 'Student'

export interface User {
  id: string
  email: string
  full_name: string
  role: Role
  is_active: boolean
  permissions: string[]
}

export interface Session {
  access_token: string
  token_type: string
  user: User
}
