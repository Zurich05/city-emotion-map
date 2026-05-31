import axios from 'axios'

export interface ApiResult<T> {
  code: number
  message: string
  data: T
  meta: Record<string, unknown>
}

const client = axios.create({ baseURL: import.meta.env.VITE_API_BASE || '', timeout: 20000 })

export async function getData<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  const response = await client.get<ApiResult<T>>(url, { params })
  if (response.data.code !== 0) throw new Error(response.data.message)
  return response.data.data
}

export async function postData<T>(url: string, data?: unknown): Promise<T> {
  const response = await client.post<ApiResult<T>>(url, data)
  if (response.data.code !== 0) throw new Error(response.data.message)
  return response.data.data
}

export default client
