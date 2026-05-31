import { defineStore } from 'pinia'

export const useFilterStore = defineStore('filter', {
  state: () => ({
    city: '武汉市',
    platform: '',
    district: '',
    emotionType: ''
  })
})
