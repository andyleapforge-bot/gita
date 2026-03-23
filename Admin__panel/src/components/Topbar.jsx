import React from 'react'
import { signOut } from 'firebase/auth'
import { auth } from '../firebase'

export default function Topbar({ title = 'Dashboard' }) {
  return (
    <header className="w-full bg-white border-b border-vitaCardBorder px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <h2 className="text-xl font-semibold text-vitaBlue-700">{title}</h2>
      </div>
      <button className="btn btn-sm btn-gold" onClick={() => signOut(auth)}>
        Logout
      </button>
    </header>
  )
}
