import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTimeline } from '../api/timeline'
import EmotionBadge from '../components/emotion/EmotionBadge'
import Spinner from '../components/ui/Spinner'
import { formatDate } from '../utils/dates'
import { BookOpen, ChevronLeft, ChevronRight } from 'lucide-react'

export default function Timeline() {
  const navigate = useNavigate()
  const [items, setItems] = useState([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const [loading, setLoading] = useState(true)

  const fetchTimeline = useCallback(async () => {
    setLoading(true)
    try {
      const res = await getTimeline({ page, page_size: 15 })
      setItems(res.data.items)
      setTotalPages(res.data.total_pages)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [page])

  useEffect(() => { fetchTimeline() }, [fetchTimeline])

  // Group by month-year
  const grouped = items.reduce((acc, item) => {
    const monthKey = item.date.slice(0, 7)
    if (!acc[monthKey]) acc[monthKey] = []
    acc[monthKey].push(item)
    return acc
  }, {})

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Timeline</h1>
      <p className="text-gray-500 text-sm mb-8">Your memory journey through time</p>

      {loading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : items.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          <BookOpen size={40} className="mx-auto mb-3 opacity-30" />
          <p>No memories yet. Start journaling to see your timeline.</p>
        </div>
      ) : (
        <>
          {Object.entries(grouped).sort(([a], [b]) => b.localeCompare(a)).map(([monthKey, monthItems]) => (
            <div key={monthKey} className="mb-10">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-px flex-1 bg-gray-200" />
                <span className="text-sm font-medium text-gray-500 bg-gray-50 px-3 py-1 rounded-full">
                  {formatMonthYear(monthKey)}
                </span>
                <div className="h-px flex-1 bg-gray-200" />
              </div>

              <div className="space-y-4 ml-4">
                {monthItems.map((item, idx) => (
                  <div key={idx} className="flex gap-4">
                    {/* Timeline line */}
                    <div className="flex flex-col items-center">
                      <div className="w-3 h-3 rounded-full bg-primary-400 mt-1.5 shrink-0 ring-4 ring-primary-50" />
                      {idx < monthItems.length - 1 && <div className="w-px flex-1 bg-gray-200 mt-1" />}
                    </div>

                    {/* Card */}
                    <div
                      className="flex-1 bg-white rounded-xl border border-gray-100 p-4 mb-4 hover:shadow-sm cursor-pointer transition-shadow"
                      onClick={() => navigate(`/journals/${item.data.id}`)}
                    >
                      <div className="flex items-start justify-between gap-3 mb-2">
                        <h3 className="font-medium text-gray-900 line-clamp-1">{item.data.title}</h3>
                        {item.data.emotion && (
                          <EmotionBadge emotion={item.data.emotion.dominant_emotion} />
                        )}
                      </div>
                      <p className="text-sm text-gray-500 line-clamp-2">{item.data.content}</p>
                      <p className="text-xs text-gray-400 mt-2">{formatDate(item.date)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-4">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="p-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50"
              >
                <ChevronLeft size={16} />
              </button>
              <span className="text-sm text-gray-600">Page {page} of {totalPages}</span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="p-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50"
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

function formatMonthYear(monthKey) {
  const [year, month] = monthKey.split('-')
  const date = new Date(parseInt(year), parseInt(month) - 1)
  return date.toLocaleString('default', { month: 'long', year: 'numeric' })
}
