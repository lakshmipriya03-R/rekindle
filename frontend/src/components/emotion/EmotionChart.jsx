import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { getEmotionColor } from '../../utils/emotions'

export default function EmotionChart({ distribution }) {
  if (!distribution || Object.keys(distribution).length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
        No emotion data yet
      </div>
    )
  }

  const data = Object.entries(distribution).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
    color: getEmotionColor(name),
  }))

  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
          {data.map((entry, i) => <Cell key={i} fill={entry.color} />)}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  )
}
