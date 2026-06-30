import client from './client'

export const getSessions = (params) => client.get('/chat/sessions', { params })
export const getSession = (id) => client.get(`/chat/sessions/${id}`)
export const createSession = (data) => client.post('/chat/sessions', data)
export const sendMessage = (data) => client.post('/chat/message', data)
