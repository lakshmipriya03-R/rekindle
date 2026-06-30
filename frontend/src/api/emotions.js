import client from './client'

export const getEmotionStats = () => client.get('/emotions/stats')
export const getEmotionTrends = () => client.get('/emotions/trends')
export const searchEmotions = (params) => client.get('/emotions', { params })
