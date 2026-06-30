import client from './client'

export const getTimeline = (params) => client.get('/timeline', { params })
