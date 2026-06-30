export function formatDate(date) {
  if (!date) return ''

  return new Date(date).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export function formatDateTime(date) {
  if (!date) return ''

  return new Date(date).toLocaleString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

export function formatRelative(date) {
  if (!date) return ''

  const d = new Date(date)
  const now = new Date()

  const today = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate()
  )

  const yesterday = new Date(today)
  yesterday.setDate(today.getDate() - 1)

  const msgDay = new Date(
    d.getFullYear(),
    d.getMonth(),
    d.getDate()
  )

  const time = d.toLocaleTimeString('en-IN', {
    hour: 'numeric',
    minute: '2-digit',
  })

  if (msgDay.getTime() === today.getTime()) {
    return `Today • ${time}`
  }

  if (msgDay.getTime() === yesterday.getTime()) {
    return `Yesterday • ${time}`
  }

  return d.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }) + ` • ${time}`
}
