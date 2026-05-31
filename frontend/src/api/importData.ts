import client, { ApiResult, getData, postData } from './request'

export async function uploadData(file: File, platform: string, replace = false) {
  const form = new FormData()
  form.append('file', file)
  form.append('platform', platform)
  form.append('replace', String(replace))
  const response = await client.post<ApiResult<Record<string, number>>>('/api/import', form)
  if (response.data.code !== 0) throw new Error(response.data.message)
  return response.data.data
}

export const importDemoData = () => postData<Record<string, number>>('/api/import/demo')
export const fetchImportLogs = (params?: Record<string, unknown>) => getData<Array<Record<string, any>>>('/api/import/logs', params)
