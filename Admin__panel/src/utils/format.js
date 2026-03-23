export function formatDate(ts) {
  try {
    const d = ts?.toDate ? ts.toDate() : new Date(ts)
    return d.toLocaleDateString()
  } catch {
    return ''
  }
}

export function monthKey(ts) {
  const d = ts?.toDate ? ts.toDate() : new Date(ts)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}
