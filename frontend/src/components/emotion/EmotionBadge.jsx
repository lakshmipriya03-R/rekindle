import { getEmotionConfig } from '../../utils/emotions'

export default function EmotionBadge({ emotion, showEmoji = true, size = 'sm' }) {
  if (!emotion) return null
  const config = getEmotionConfig(emotion)
  const sizes = { sm: 'text-xs px-2 py-0.5', md: 'text-sm px-3 py-1' }

  return (
    <span className={`inline-flex items-center gap-1 rounded-full font-medium ${config.bg} ${config.text} ${sizes[size]}`}>
      {showEmoji && <span>{config.emoji}</span>}
      {config.label}
    </span>
  )
}
