import client from './client'

export const getJournals = (params) => client.get('/journals', { params })
export const getJournal = (id) => client.get(`/journals/${id}`)
export const createJournal = (data) => client.post('/journals', data)
export const updateJournal = (id, data) => client.patch(`/journals/${id}`, data)
export const deleteJournal = (id) => client.delete(`/journals/${id}`)
