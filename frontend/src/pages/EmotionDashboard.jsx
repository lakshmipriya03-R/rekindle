import { useState, useEffect } from 'react'
import { getEmotionStats, getEmotionTrends, searchEmotions } from '../api/emotions'
import EmotionChart from '../components/emotion/EmotionChart'
import EmotionBadge from '../components/emotion/EmotionBadge'
import Spinner from '../components/ui/Spinner'
import { formatDateTime } from '../utils/dates'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { getEmotionColor } from '../utils/emotions'

export default function EmotionDashboard() {
  const [stats, setStats] = useState(null)
  const [trends, setTrends] = useState([])
  const [recent, setRecent] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getEmotionStats(),
      getEmotionTrends(),
      searchEmotions({ page: 1, page_size: 10 }),
    ])
      .then(([s, t, r]) => {
        setStats(s.data)
        setTrends(t.data)
        setRecent(r.data.items || [])
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="flex-1 flex items-center justify-center"><Spinner size="lg" /></div>

  const barData = stats
    ? Object.entries(stats.emotion_distribution).map(([name, count]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        count,
        emotion: name,
      }))
    : []

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Emotion Dashboard</h1>
      <p className="text-gray-500 text-sm mb-8">Understanding your emotional journey</p>

      {/* Summary cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total tracked', value: stats?.total_entries || 0 },
          { label: 'Most common', value: stats?.dominant_overall ? stats.dominant_overall.charAt(0).toUpperCase() + stats.dominant_overall.slice(1) : '—' },
          { label: 'Avg joy', value: `${((stats?.average_joy || 0) * 100).toFixed(0)}%` },
          { label: 'Avg sadness', value: `${((stats?.average_sadness || 0) * 100).toFixed(0)}%` },
        ].map(({ label, value }) => (
          <div key={label} className="bg-white rounded-xl border border-gray-100 p-5">
            <p className="text-2xl font-bold text-gray-900">{value}</p>
            <p className="text-sm text-gray-500">{label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Pie chart */}
        <div className="bg-white rounded-xl border border-gray-100 p-6">
          <h2 className="font-semibold text-gray-900 mb-4">Emotion Distribution</h2>
          <EmotionChart distribution={stats?.emotion_distribution} />
        </div>

        {/* Bar chart */}
        <div className="bg-white rounded-xl border border-gray-100 p-6">
          <h2 className="font-semibold text-gray-900 mb-4">Count by Emotion</h2>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={barData} margin={{ top: 5, right: 10, bottom: 5, left: 0 }}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={getEmotionColor(entry.emotion)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent emotion analyses */}
      <div className="bg-white rounded-xl border border-gray-100 p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Recent Analyses</h2>
        {recent.length === 0 ? (
          <p className="text-sm text-gray-400 text-center py-6">No analyses yet</p>
        ) : (
          <div className="space-y-3">
            {recent.map((a) => (
              <div key={a.id} className="flex items-center gap-3 p-3 rounded-lg bg-gray-50">
                <EmotionBadge emotion={a.dominant_emotion} />
                <span className="text-xs text-gray-400 flex-1 capitalize">{a.source_type}</span>
                <span className="text-xs text-gray-400">{((a.confidence || 0) * 100).toFixed(0)}% confidence</span>
                <span className="text-xs text-gray-400">{formatDateTime(a.analyzed_at)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
