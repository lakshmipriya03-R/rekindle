import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || ''

const client = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
  failedQueue = []
}

client.interceptors.response.use(
  (res) => res,
  async (error) => {
    const orig = error.config
    if (error.response?.status === 401 && !orig._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => failedQueue.push({ resolve, reject }))
          .then((token) => { orig.headers.Authorization = `Bearer ${token}`; return client(orig) })
          .catch((e) => Promise.reject(e))
      }
      orig._retry = true
      isRefreshing = true
      const rt = localStorage.getItem('refresh_token')
      if (!rt) { isRefreshing = false; window.location.href = '/login'; return Promise.reject(error) }
      try {
        const { data } = await axios.post(`${BASE_URL}/auth/refresh`, { refresh_token: rt })
        localStorage.setItem('access_token', data.access_token)
        processQueue(null, data.access_token)
        orig.headers.Authorization = `Bearer ${data.access_token}`
        return client(orig)
      } catch (e) {
        processQueue(e, null)
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)

export default client
