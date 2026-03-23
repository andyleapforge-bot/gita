import React from 'react'

export default function Modal({ open, title, children, onClose }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="card w-full max-w-lg">
        <div className="flex items-center justify-between px-4 py-3 border-b">
          <h3 className="font-semibold">{title}</h3>
          <button className="btn btn-ghost" onClick={onClose}>✖</button>
        </div>
        <div className="p-4">{children}</div>
      </div>
    </div>
  )
}
