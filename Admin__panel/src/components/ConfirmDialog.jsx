import React from 'react'

export default function ConfirmDialog({ open, title = 'Confirm', message, onConfirm, onCancel }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="card w-full max-w-md">
        <div className="px-4 py-3 border-b">
          <h3 className="font-semibold">{title}</h3>
        </div>
        <div className="p-4 space-y-4">
          <p>{message}</p>
          <div className="flex justify-end gap-2">
            <button className="btn" onClick={onCancel}>Cancel</button>
            <button className="btn-gold" onClick={onConfirm}>Confirm</button>
          </div>
        </div>
      </div>
    </div>
  )
}
