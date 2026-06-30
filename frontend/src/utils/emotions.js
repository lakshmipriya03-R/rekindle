export const EMOTION_CONFIG = {
  joy: { label: 'Joy', color: '#f59e0b', bg: 'bg-amber-100', text: 'text-amber-700', emoji: '😊' },
  sadness: { label: 'Sadness', color: '#3b82f6', bg: 'bg-blue-100', text: 'text-blue-700', emoji: '😢' },
  fear: { label: 'Fear', color: '#8b5cf6', bg: 'bg-violet-100', text: 'text-violet-700', emoji: '😨' },
  anger: { label: 'Anger', color: '#ef4444', bg: 'bg-red-100', text: 'text-red-700', emoji: '😠' },
  surprise: { label: 'Surprise', color: '#ec4899', bg: 'bg-pink-100', text: 'text-pink-700', emoji: '😲' },
  disgust: { label: 'Disgust', color: '#10b981', bg: 'bg-emerald-100', text: 'text-emerald-700', emoji: '🤢' },
  neutral: { label: 'Neutral', color: '#6b7280', bg: 'bg-gray-100', text: 'text-gray-700', emoji: '😐' },
}
export const getEmotionConfig = (emotion) => EMOTION_CONFIG[emotion?.toLowerCase()] || EMOTION_CONFIG.neutral
export const getEmotionColor = (emotion) => getEmotionConfig(emotion).color
