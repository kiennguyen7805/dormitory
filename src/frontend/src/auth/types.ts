export type Role = 'Admin' | 'Staff' | 'Student'

export interface User {
  id: string
  email: string
  full_name: string
  role: Role
}

export interface Session {
  access_token: string
  token_type: string
  user: User
}
