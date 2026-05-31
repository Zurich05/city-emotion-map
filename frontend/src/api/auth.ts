import { postData } from './request'

export interface LoginResult {
  access_token: string
  token_type: string
}

export async function login(username: string, password: string) {
  const result = await postData<LoginResult>('/api/auth/login', { username, password })
  localStorage.setItem('access_token', result.access_token)
  return result
}

export function logout() {
  localStorage.removeItem('access_token')
}
