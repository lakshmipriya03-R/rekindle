import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getJournals, deleteJournal } from '../api/journals'
import JournalCard from '../components/journal/JournalCard'
import SearchBar from '../components/journal/SearchBar'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import { PenLine, ChevronLeft, ChevronRight } from 'lucide-react'

const EMOTIONS = ['joy', 'sadness', 'fear', 'anger', 'surprise', 'disgust', 'neutral']

export default function Journal() {
  const navigate = useNavigate()
  const [journals, setJournals] = useState([])
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [emotion, setEmotion] = useState('')
  const [loading, setLoading] = useState(true)
  const PAGE_SIZE = 9

  const fetchJournals = useCallback(async () => {
    setLoading(true)
    try {
      const params = { page, page_size: PAGE_SIZE }
      if (search) params.search = search
      if (emotion) params.emotion = emotion
      const res = await getJournals(params)
      setJournals(res.data.items)
      setTotal(res.data.total)
      setTotalPages(res.data.total_pages)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [page, search, emotion])

  useEffect(() => { fetchJournals() }, [fetchJournals])

  // Reset to page 1 when filters change
  useEffect(() => { setPage(1) }, [search, emotion])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this journal entry?')) return
    await deleteJournal(id)
    fetchJournals()
  }

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Journal</h1>
          <p className="text-gray-500 text-sm mt-1">{total} {total === 1 ? 'entry' : 'entries'}</p>
        </div>
        <Button onClick={() => navigate('/journals/new')}>
          <PenLine size={16} /> New Entry
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="flex-1">
          <SearchBar value={search} onChange={setSearch} />
        </div>
        <select
          value={emotion}
          onChange={(e) => setEmotion(e.target.value)}
          className="px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white text-gray-700"
        >
          <option value="">All emotions</option>
          {EMOTIONS.map((e) => (
            <option key={e} value={e}>{e.charAt(0).toUpperCase() + e.slice(1)}</option>
          ))}
        </select>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : journals.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          <p className="text-lg mb-2">No entries found</p>
          <p className="text-sm mb-6">
            {search || emotion ? 'Try changing your search or filter' : 'Start writing your first memory'}
          </p>
          {!search && !emotion && (
            <Button onClick={() => navigate('/journals/new')}>Write your first entry</Button>
          )}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {journals.map((j) => (
              <JournalCard key={j.id} journal={j} onDelete={handleDelete} />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-8">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="p-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50 transition-colors"
              >
                <ChevronLeft size={16} />
              </button>
              <span className="text-sm text-gray-600">Page {page} of {totalPages}</span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="p-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50 transition-colors"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
