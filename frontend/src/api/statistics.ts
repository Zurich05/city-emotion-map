import { getData } from './request'

export interface Overview {
  total_count: number
  today_count: number
  positive_ratio: number
  negative_ratio: number
  neutral_ratio: number
  avg_sentiment_score: number
  avg_stress_score: number
  avg_joy_score: number
  high_risk_count: number
}

export const fetchOverview = () => getData<Overview>('/api/statistics/overview')
export const fetchPlatform = () => getData<Array<Record<string, any>>>('/api/statistics/platform')
export const fetchTimeline = () => getData<Array<Record<string, any>>>('/api/statistics/timeline')
export const fetchDistrictRank = () => getData<Array<Record<string, any>>>('/api/statistics/district-rank')
export const fetchHotspots = () => getData<Array<Record<string, any>>>('/api/hotspots')
export const fetchReport = () => getData<Record<string, any>>('/api/report')
