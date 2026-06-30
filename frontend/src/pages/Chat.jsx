import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getSessions, getSession, sendMessage } from '../api/chat'
import ChatBubble from '../components/chat/ChatBubble'
import ChatInput from '../components/chat/ChatInput'
import Spinner from '../components/ui/Spinner'
import { Plus, MessageCircle } from 'lucide-react'
import { formatRelative } from '../utils/dates'

export default function Chat() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const [sessions, setSessions] = useState([])
  const [activeSession, setActiveSession] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    getSessions({ page: 1, page_size: 30 })
      .then((res) => setSessions(res.data.items || []))
      .catch(console.error)
  }, [])

  useEffect(() => {
    if (!sessionId) return
    setLoading(true)
    getSession(sessionId)
      .then((res) => {
        setActiveSession(res.data)
        setMessages(res.data.messages || [])
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [sessionId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (content) => {
    setSending(true)
    try {
      const res = await sendMessage({
        content,
        session_id: sessionId ? parseInt(sessionId) : null,
      })
      const { session_id, user_message, assistant_message } = res.data

      if (!sessionId) {
        navigate(`/chat/${session_id}`, { replace: true })
        getSessions({ page: 1, page_size: 30 }).then((r) => setSessions(r.data.items || []))
      }

      setMessages((prev) => [...prev, user_message, assistant_message])
   } catch (e) {
  console.error("CHAT ERROR:", e)
  alert(JSON.stringify(e.response?.data || e.message))
} finally {
      setSending(false)
    }
  }

  return (
    <div className="flex h-full">
      {/* Session list */}
      <aside className="w-72 border-r border-gray-100 bg-white flex flex-col">
        <div className="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="font-semibold text-gray-900">Conversations</h2>
          <button
            onClick={() => navigate('/chat')}
            className="w-8 h-8 bg-primary-600 text-white rounded-lg flex items-center justify-center hover:bg-primary-700 transition-colors"
            title="New conversation"
          >
            <Plus size={16} />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {sessions.length === 0 ? (
            <p className="text-sm text-gray-400 text-center p-6">No conversations yet</p>
          ) : (
            sessions.map((s) => (
              <button
                key={s.id}
                onClick={() => navigate(`/chat/${s.id}`)}
                className={`w-full text-left px-4 py-3 border-b border-gray-50 hover:bg-gray-50 transition-colors ${
                  s.id === parseInt(sessionId) ? 'bg-primary-50' : ''
                }`}
              >
                <p className="text-sm font-medium text-gray-800 truncate">{s.title}</p>
                <p className="text-xs text-gray-400 mt-0.5">{formatRelative(s.updated_at)}</p>
              </button>
            ))
          )}
        </div>
      </aside>

      {/* Chat area */}
      <div className="flex-1 flex flex-col">
        {!sessionId ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
            <div className="w-16 h-16 bg-primary-50 rounded-full flex items-center justify-center mb-4">
              <MessageCircle size={28} className="text-primary-600" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Talk to Rekindle</h2>
            <p className="text-gray-500 text-sm max-w-sm mb-8">
              Your compassionate AI companion is here to listen, remember, and reconnect with your memories.
            </p>
            <ChatInput onSend={handleSend} loading={sending} />
          </div>
        ) : loading ? (
          <div className="flex-1 flex items-center justify-center"><Spinner size="lg" /></div>
        ) : (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {messages.length === 0 && (
                <p className="text-center text-gray-400 text-sm mt-8">Start the conversation below</p>
              )}
              {messages.map((msg) => <ChatBubble key={msg.id} message={msg} />)}
              {sending && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-warm-100 flex items-center justify-center shrink-0">
                    <Spinner size="sm" />
                  </div>
                  <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 text-gray-400 text-sm shadow-sm">
                    Rekindle is thinking...
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <ChatInput onSend={handleSend} loading={sending} />
          </>
        )}
      </div>
    </div>
  )
}
