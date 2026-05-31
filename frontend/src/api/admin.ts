import client, { getData } from './request'

export const fetchAuditLogs = (params?: Record<string, unknown>) => getData<Array<Record<string, any>>>('/api/audit/logs', params)

export async function downloadBackup() {
  const response = await client.get('/api/backup/export', { responseType: 'blob' })
  const blob = new Blob([response.data], { type: 'application/json;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = 'city-emotion-backup.json'
  anchor.click()
  URL.revokeObjectURL(url)
}

export async function restoreBackup(file: File, replace = false) {
  const form = new FormData()
  form.append('file', file)
  form.append('replace', String(replace))
  const response = await client.post('/api/backup/restore', form)
  return response.data.data
}
