import { useState } from 'react'
import { Send } from 'lucide-react'

export default function ChatInput({ onSend, loading }) {
  const [text, setText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!text.trim() || loading) return
    onSend(text.trim())
    setText('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-3 p-4 border-t border-gray-100 bg-white">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Share a memory or thought..."
        rows={1}
        className="flex-1 resize-none px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm bg-gray-50 max-h-32"
        style={{ height: 'auto', minHeight: '44px' }}
        onInput={(e) => {
          e.target.style.height = 'auto'
          e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px'
        }}
      />
      <button
        type="submit"
        disabled={!text.trim() || loading}
        className="w-10 h-10 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl flex items-center justify-center transition-colors shrink-0"
      >
        <Send size={16} />
      </button>
    </form>
  )
}
