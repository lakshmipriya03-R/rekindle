import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getJournal, createJournal, updateJournal } from '../api/journals'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import EmotionBadge from '../components/emotion/EmotionBadge'
import Spinner from '../components/ui/Spinner'
import { ArrowLeft, Save, Heart } from 'lucide-react'
import { formatDate } from '../utils/dates'

export default function JournalEntry() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEditing = !!id

  const [form, setForm] = useState({ title: '', content: '', mood_score: '' })
  const [emotion, setEmotion] = useState(null)
  const [loading, setLoading] = useState(isEditing)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')
  const [createdAt, setCreatedAt] = useState(null)

  useEffect(() => {
    if (!isEditing) return
    getJournal(id)
      .then((res) => {
        const j = res.data
        setForm({ title: j.title, content: j.content, mood_score: j.mood_score || '' })
        setEmotion(j.emotion)
        setCreatedAt(j.created_at)
      })
      .catch(() => navigate('/journals'))
      .finally(() => setLoading(false))
  }, [id, isEditing, navigate])

  const handleSave = async () => {
    if (!form.title.trim() || !form.content.trim()) {
      setError('Title and content are required')
      return
    }
    setSaving(true)
    setError('')
    try {
      const payload = {
        title: form.title.trim(),
        content: form.content.trim(),
        mood_score: form.mood_score ? parseInt(form.mood_score) : null,
      }
      if (isEditing) {
        await updateJournal(id, payload)
      } else {
        const res = await createJournal(payload)
        navigate(`/journals/${res.data.id}`, { replace: true })
      }
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to save')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="flex-1 flex items-center justify-center"><Spinner size="lg" /></div>

  return (
    <div className="p-8 max-w-3xl mx-auto">
      {/* Top bar */}
      <div className="flex items-center gap-4 mb-8">
        <button onClick={() => navigate('/journals')} className="text-gray-400 hover:text-gray-600 transition-colors">
          <ArrowLeft size={20} />
        </button>
        <div className="flex-1" />
        {emotion && <EmotionBadge emotion={emotion.dominant_emotion} size="md" />}
        {createdAt && <span className="text-sm text-gray-400">{formatDate(createdAt)}</span>}
        <Button onClick={handleSave} loading={saving} size="sm">
          <Save size={15} />
          {saved ? 'Saved!' : isEditing ? 'Save changes' : 'Save entry'}
        </Button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-100 rounded-lg text-red-700 text-sm">{error}</div>
      )}

      {/* Title */}
      <input
        type="text"
        placeholder="Entry title..."
        value={form.title}
        onChange={(e) => setForm({ ...form, title: e.target.value })}
        className="w-full text-3xl font-bold text-gray-900 placeholder-gray-300 border-none outline-none bg-transparent mb-4 resize-none"
      />

      {/* Mood score */}
      <div className="flex items-center gap-2 mb-6">
        <Heart size={16} className="text-gray-400" />
        <span className="text-sm text-gray-500">Mood:</span>
        <div className="flex gap-1">
          {[1,2,3,4,5,6,7,8,9,10].map((n) => (
            <button
              key={n}
              onClick={() => setForm({ ...form, mood_score: form.mood_score === n ? '' : n })}
              className={`w-7 h-7 rounded-full text-xs font-medium transition-colors ${
                form.mood_score === n
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-500 hover:bg-primary-100'
              }`}
            >
              {n}
            </button>
          ))}
        </div>
        {form.mood_score && (
          <span className="text-xs text-gray-400 ml-1">{form.mood_score}/10</span>
        )}
      </div>

      {/* Divider */}
      <div className="border-t border-gray-100 mb-6" />

      {/* Content */}
      <textarea
        placeholder="Write your memory here... What happened today? What are you feeling? What do you remember?"
        value={form.content}
        onChange={(e) => setForm({ ...form, content: e.target.value })}
        className="w-full text-gray-700 leading-relaxed placeholder-gray-300 border-none outline-none bg-transparent resize-none text-lg min-h-96"
        rows={20}
      />
    </div>
  )
}
