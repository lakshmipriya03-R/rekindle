import { useNavigate } from 'react-router-dom'
import { formatRelative } from '../../utils/dates'
import EmotionBadge from '../emotion/EmotionBadge'
import { Heart } from 'lucide-react'

export default function JournalCard({ journal, onDelete }) {
  const navigate = useNavigate()

  return (
    <div
      className="bg-white rounded-xl border border-gray-100 p-5 hover:shadow-md transition-shadow cursor-pointer group"
      onClick={() => navigate(`/journals/${journal.id}`)}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <h3 className="font-semibold text-gray-900 group-hover:text-primary-700 transition-colors line-clamp-1">
          {journal.title}
        </h3>
        {journal.emotion && <EmotionBadge emotion={journal.emotion.dominant_emotion} />}
      </div>

      <p className="text-gray-500 text-sm line-clamp-3 mb-4">{journal.content}</p>

      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-400">{formatRelative(journal.created_at)}</span>
        <div className="flex items-center gap-3">
          {journal.mood_score && (
            <div className="flex items-center gap-1 text-xs text-gray-400">
              <Heart size={12} />
              <span>{journal.mood_score}/10</span>
            </div>
          )}
          <button
            onClick={(e) => { e.stopPropagation(); onDelete(journal.id) }}
            className="text-xs text-gray-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}
