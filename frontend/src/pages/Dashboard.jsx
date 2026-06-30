import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getDashboardStats } from '../api/dashboard'
import { formatRelative } from '../utils/dates'
import EmotionBadge from '../components/emotion/EmotionBadge'
import EmotionChart from '../components/emotion/EmotionChart'
import Spinner from '../components/ui/Spinner'
import Button from '../components/ui/Button'
import { BookOpen, MessageCircle, BarChart2, PenLine, LineChart } from 'lucide-react'
import { LineChart as ReLineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

function StatCard({ icon: Icon, label, value, color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-50 text-primary-600',
    amber: 'bg-amber-50 text-amber-600',
    blue: 'bg-blue-50 text-blue-600',
  }
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-5 flex items-center gap-4">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${colors[color]}`}>
        <Icon size={20} />
      </div>
      <div>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        <p className="text-sm text-gray-500">{label}</p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getDashboardStats()
      .then((res) => setStats(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="flex-1 flex items-center justify-center"><Spinner size="lg" /></div>

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Good {getGreeting()}, {user?.full_name?.split(' ')[0]} 👋
          </h1>
          <p className="text-gray-500 mt-1">Here's what's been happening with your memories</p>
        </div>
        <Button onClick={() => navigate('/journals/new')} className="flex items-center gap-2">
          <PenLine size={16} /> New Entry
        </Button>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <StatCard icon={BookOpen} label="Journal Entries" value={stats?.total_journals ?? 0} color="primary" />
        <StatCard icon={MessageCircle} label="Conversations" value={stats?.total_sessions ?? 0} color="blue" />
        <StatCard icon={BarChart2} label="Emotions Tracked" value={stats?.total_messages ?? 0} color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Emotion Distribution */}
        <div className="bg-white rounded-xl border border-gray-100 p-6">
          <h2 className="font-semibold text-gray-900 mb-4">Emotions (last 30 days)</h2>
          <EmotionChart distribution={stats?.emotion_distribution_30d} />
        </div>

        {/* Mood Trend */}
        <div className="bg-white rounded-xl border border-gray-100 p-6">
          <h2 className="font-semibold text-gray-900 mb-4">Mood Trend (last 30 days)</h2>
          {stats?.mood_trend_30d?.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <ReLineChart data={stats.mood_trend_30d}>
                <XAxis dataKey="date" tick={{ fontSize: 11 }} tickFormatter={(d) => d.slice(5)} />
                <YAxis domain={[1, 10]} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Line type="monotone" dataKey="avg_mood" stroke="#c026d3" strokeWidth={2} dot={false} />
              </ReLineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
              No mood data yet — add a mood score to your journal entries
            </div>
          )}
        </div>
      </div>

      {/* Recent Journals */}
      <div className="bg-white rounded-xl border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-gray-900">Recent Journal Entries</h2>
          <button onClick={() => navigate('/journals')} className="text-sm text-primary-600 hover:text-primary-700">
            View all
          </button>
        </div>
        {stats?.recent_journals?.length > 0 ? (
          <div className="space-y-3">
            {stats.recent_journals.map((j) => (
              <div
                key={j.id}
                onClick={() => navigate(`/journals/${j.id}`)}
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <div className="w-2 h-2 rounded-full bg-primary-400 shrink-0" />
                <span className="text-sm font-medium text-gray-800 flex-1 truncate">{j.title}</span>
                {j.emotion && <EmotionBadge emotion={j.emotion.dominant_emotion} showEmoji={false} />}
                <span className="text-xs text-gray-400 shrink-0">{formatRelative(j.created_at)}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-400 text-center py-8">
            No journal entries yet.{' '}
            <button onClick={() => navigate('/journals/new')} className="text-primary-600 hover:underline">
              Write your first one
            </button>
          </p>
        )}
      </div>
    </div>
  )
}

function getGreeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 17) return 'afternoon'
  return 'evening'
}
