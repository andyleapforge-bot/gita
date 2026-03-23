import React, { useState } from 'react'
import Modal from '../components/Modal'
import { changeEmail, changePassword, reauthenticate } from '../services/adminService'

export default function Settings() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [reauthOpen, setReauthOpen] = useState(false)
  const [reauthFor, setReauthFor] = useState(null) // 'email' | 'password'
  const [reauthPassword, setReauthPassword] = useState('')
  const [toast, setToast] = useState('')

  async function requestReauth(kind) {
    setReauthFor(kind)
    setReauthOpen(true)
  }

  async function doReauthAndRun() {
    try {
      await reauthenticate(reauthPassword)
      setReauthOpen(false)
      setReauthPassword('')
      if (reauthFor === 'email') {
        await changeEmail(email.trim())
        setToast('Email updated')
        setEmail('')
      } else if (reauthFor === 'password') {
        await changePassword(password)
        setToast('Password updated')
        setPassword('')
      }
    } catch (e) {
      setToast(e.message)
    }
  }

  return (
    <div className="space-y-6">
      {toast && (
        <div className="alert alert-info">
          <span>{toast}</span>
        </div>
      )}

      <div className="card p-4">
        <h3 className="font-semibold mb-3">Change Email</h3>
        <div className="flex gap-3">
          <input className="input input-bordered flex-1" placeholder="New email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <button className="btn-gold" onClick={() => requestReauth('email')}>Update Email</button>
        </div>
      </div>

      <div className="card p-4">
        <h3 className="font-semibold mb-3">Change Password</h3>
        <div className="flex gap-3">
          <input className="input input-bordered flex-1" type="password" placeholder="New password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="btn-gold" onClick={() => requestReauth('password')}>Update Password</button>
        </div>
      </div>

      <Modal open={reauthOpen} title="Re-authentication Required" onClose={() => setReauthOpen(false)}>
        <div className="space-y-3">
          <p>Please enter your current password to proceed.</p>
          <input className="input input-bordered w-full" type="password" placeholder="Current password" value={reauthPassword} onChange={(e) => setReauthPassword(e.target.value)} />
          <div className="flex justify-end gap-2">
            <button className="btn" onClick={() => setReauthOpen(false)}>Cancel</button>
            <button className="btn-gold" onClick={doReauthAndRun}>Confirm</button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
