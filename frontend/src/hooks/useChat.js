import { useState, useCallback } from 'react'
import { sendMessage } from '../api/chat'

export function useChat(sessionId) {
  const [messages, setMessages] = useState([])
  const [sending, setSending] = useState(false)
  const [error, setError] = useState(null)

  const send = useCallback(async (content) => {
    setSending(true)
    setError(null)
    try {
      const res = await sendMessage({ content, session_id: sessionId || null })
      const { user_message, assistant_message } = res.data
      setMessages((prev) => [...prev, user_message, assistant_message])
      return res.data
    } catch (e) {
      setError(e)
      throw e
    } finally {
      setSending(false)
    }
  }, [sessionId])

  return { messages, setMessages, sending, error, send }
}
