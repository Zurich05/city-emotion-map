import { postData } from './request'

export const startCrawl = (payload: { platform: string; keyword: string; limit: number }) => postData<Record<string, number>>('/api/crawl/start', payload)
export const runClean = () => postData<Record<string, number>>('/api/clean/run')
export const runSentiment = () => postData<Record<string, number>>('/api/sentiment/run')
