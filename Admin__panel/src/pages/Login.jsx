import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginAdmin, requestPasswordReset } from '../services/adminService'

export default function Login() {
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState('')
  const [toastType, setToastType] = useState('warning')
  const [resetSent, setResetSent] = useState(false)

  async function onLogin(e) {
    e.preventDefault()
    setLoading(true)
    setToast('')
    try {
      await loginAdmin(email.trim(), password)
      nav('/')
    } catch (err) {
      const code = err?.code || ''
      if (
        code === 'auth/invalid-login-credentials' ||
        code === 'auth/user-not-found' ||
        code === 'auth/wrong-password'
      ) {
        setToast('Invalid email or password. Use "Forgot Password" to reset your credentials.')
      } else {
        setToast(err.message)
      }
      setToastType('warning')
    } finally {
      setLoading(false)
    }
  }

  async function onForgotPassword() {
    const trimmedEmail = email.trim()
    if (!trimmedEmail) {
      setToast('Enter your email address above, then click Forgot Password.')
      setToastType('warning')
      return
    }
    setLoading(true)
    try {
      await requestPasswordReset(trimmedEmail)
      setResetSent(true)
      setToast(`Password reset email sent to ${trimmedEmail}. Check your inbox.`)
      setToastType('success')
    } catch (err) {
      setToast(err.message)
      setToastType('warning')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen w-full app-shell grid place-items-center">
      <div className="card w-full max-w-md p-6 bg-white/90 backdrop-blur-sm">
        <h2 className="text-2xl font-bold mb-4 text-vitaBlue-800">VitaGita Admin Login</h2>
        {toast && (
          <div className={`alert ${toastType === 'success' ? 'alert-success' : 'alert-warning'} mb-3`}>
            <span>{toast}</span>
          </div>
        )}
        <form onSubmit={onLogin} className="space-y-3">
          <input
            className="input input-bordered w-full"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            className="input input-bordered w-full"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button className="btn-gold w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Login'}
          </button>
        </form>
        <div className="mt-3 text-center">
          <button
            type="button"
            className="text-sm text-vitaBlue-700 underline hover:text-vitaBlue-900 disabled:opacity-50"
            onClick={onForgotPassword}
            disabled={loading || resetSent}
          >
            Forgot Password?
          </button>
        </div>
      </div>
    </div>
  )
}
