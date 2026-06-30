import client from './client'

export const register = (data) => client.post('/auth/register', data)
export const login = (data) => client.post('/auth/login', data)
export const logout = (refreshToken) => client.post('/auth/logout', { refresh_token: refreshToken })
export const getMe = () => client.get('/users/me')
export const updateMe = (data) => client.patch('/users/me', data)
export const changePassword = (data) => client.put('/users/me/password', data)
export const deleteAccount = () => client.delete('/users/me')
