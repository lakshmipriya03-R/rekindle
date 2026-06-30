import { useState, useEffect, useCallback } from 'react'
import { getJournals, deleteJournal } from '../api/journals'

export function useJournals({ page = 1, pageSize = 10, search = '', emotion = '' } = {}) {
  const [journals, setJournals] = useState([])
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = { page, page_size: pageSize }
      if (search) params.search = search
      if (emotion) params.emotion = emotion
      const res = await getJournals(params)
      setJournals(res.data.items)
      setTotal(res.data.total)
      setTotalPages(res.data.total_pages)
    } catch (e) {
      setError(e)
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, search, emotion])

  useEffect(() => { fetch() }, [fetch])

  const remove = useCallback(async (id) => {
    await deleteJournal(id)
    fetch()
  }, [fetch])

  return { journals, total, totalPages, loading, error, refetch: fetch, remove }
}
