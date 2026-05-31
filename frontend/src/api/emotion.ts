import { getData } from './request'

export interface EmotionPoint {
  id: number
  text: string
  platform: string
  city?: string
  district?: string
  location_name?: string
  lat?: number
  lng?: number
  sentiment_label: string
  sentiment_score: number
  stress_score: number
  joy_score: number
  anger_score: number
  calm_score: number
}

export const fetchEmotions = (params?: Record<string, unknown>) => getData<EmotionPoint[]>('/api/emotions', params)
