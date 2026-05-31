import { postData } from './request'

export interface LoginResult {
  access_token: string
  token_type: string
  role: 'admin' | 'analyst' | 'viewer'
}

export async function login(username: string, password: string) {
  const result = await postData<LoginResult>('/api/auth/login', { username, password })
  localStorage.setItem('access_token', result.access_token)
  localStorage.setItem('user_role', result.role)
  return result
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_role')
}

export function currentRole() {
  return localStorage.getItem('user_role') || 'viewer'
}
