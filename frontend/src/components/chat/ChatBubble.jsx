import { formatRelative } from '../../utils/dates'
import { Flame, Copy, Pencil, Trash2 } from 'lucide-react'

export default function ChatBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`group flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>

      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
          isUser ? 'bg-primary-100' : 'bg-warm-100'
        }`}
      >
        {isUser ? (
          <span className="text-primary-700 text-xs font-bold">You</span>
        ) : (
          <Flame size={14} className="text-warm-500" />
        )}
      </div>

      {/* Message */}
      <div
        className={`max-w-[75%] flex flex-col ${
          isUser ? 'items-end' : 'items-start'
        }`}
      >

        {/* Bubble */}
        <div
          className={`relative px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-sm ${
            isUser
              ? 'bg-primary-600 text-white rounded-tr-sm'
              : 'bg-white border border-gray-100 text-gray-800 rounded-tl-sm'
          }`}
        >
          {message.content}
        </div>

        {/* Footer */}
        <div className="flex items-center gap-3 mt-1 px-1">

          <span className="text-xs text-gray-400">
            {formatRelative(message.created_at)}
          </span>

          <div className="hidden group-hover:flex items-center gap-2 text-gray-400">

            <button className="hover:text-primary-600 transition">
              <Copy size={14} />
            </button>

            {isUser && (
              <>
                <button className="hover:text-blue-600 transition">
                  <Pencil size={14} />
                </button>

                <button className="hover:text-red-600 transition">
                  <Trash2 size={14} />
                </button>
              </>
            )}

          </div>

        </div>

      </div>

    </div>
  )
}