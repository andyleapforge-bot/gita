import React, { useEffect, useState } from 'react'
import StatsCard from '../components/StatsCard'
import { listUsers } from '../services/userService'
import { listShloks } from '../services/shlokService'
import { PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#157fc3', '#126aa8', '#0f4d7a', '#0b3350', '#071f32', '#F0C419']

export default function Dashboard() {
  const [users, setUsers] = useState([])
  const [shloks, setShloks] = useState([])
  const [bookmarks, setBookmarks] = useState(0)

  useEffect(() => {
    (async () => {
      const u = await listUsers()
      const s = await listShloks()
      setUsers(u)
      setShloks(s)
      setBookmarks(u.reduce((acc, it) => acc + (Array.isArray(it.bookmarks) ? it.bookmarks.length : 0), 0))
    })()
  }, [])

  // Removed theme/chapter breakdowns per request
  const uniqueThemes = 0

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="badge-card p-4">
          <div className="text-sm text-gray-500">Total Users</div>
          <div className="mt-1 text-2xl font-bold">{users.length}</div>
        </div>
        <div className="badge-card p-4">
          <div className="text-sm text-gray-500">Total Shloks</div>
          <div className="mt-1 text-2xl font-bold">{shloks.length}</div>
        </div>
        <div className="badge-card p-4">
          <div className="text-sm text-gray-500">Total Bookmarks</div>
          <div className="mt-1 text-2xl font-bold">{bookmarks}</div>
        </div>
        <div className="badge-card p-4">
          <div className="text-sm text-gray-500">Unique Themes</div>
          <div className="mt-1 text-2xl font-bold">{uniqueThemes}</div>
        </div>
      </div>

      {/* Users section under the 4 boxes */}
      <div className="card p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold">Recent Users</h3>
          <span className="badge-pill">Users</span>
        </div>
        <div className="overflow-x-auto">
          <table className="table w-full">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {users
                .slice()
                .sort((a, b) => {
                  const ad = a.createdAt ? new Date(a.createdAt) : new Date(0)
                  const bd = b.createdAt ? new Date(b.createdAt) : new Date(0)
                  return bd - ad
                })
                .slice(0, 8)
                .map((u, idx) => (
                  <tr key={(u.id || u.email || idx) + '-recent'}>
                    <td>{u.name || '-'}</td>
                    <td>{u.email || '-'}</td>
                    <td>{u.createdAt ? new Date(u.createdAt).toLocaleDateString() : '-'}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
