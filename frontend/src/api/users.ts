import { getData, postData } from './request'
import client from './request'

export interface UserRecord {
  id: number
  username: string
  role: 'admin' | 'analyst' | 'viewer'
  is_active: boolean
  created_at: string
}

export const fetchUsers = () => getData<UserRecord[]>('/api/users')

export const createUser = (payload: { username: string; password: string; role: string }) =>
  postData<UserRecord>('/api/users', payload)

export async function updateUser(id: number, payload: Partial<{ password: string; role: string; is_active: boolean }>) {
  const response = await client.patch(`/api/users/${id}`, payload)
  return response.data.data as UserRecord
}
