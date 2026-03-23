import React, { useEffect, useMemo, useState } from 'react'
import { listUsers } from '../services/userService'
import { listShloks } from '../services/shlokService'
import { monthKey } from '../utils/format'
import { PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#157fc3', '#126aa8', '#0f4d7a', '#0b3350', '#071f32', '#F0C419']

export default function Analytics() {
  const [users, setUsers] = useState([])
  const [shloks, setShloks] = useState([])

  useEffect(() => {
    (async () => {
      setUsers(await listUsers())
      setShloks(await listShloks())
    })()
  }, [])

  const growth = useMemo(() => {
    const map = users.reduce((acc, u) => {
      const k = monthKey(u.createdAt || new Date())
      acc[k] = (acc[k] || 0) + 1
      return acc
    }, {})
    return Object.entries(map).map(([month, count]) => ({ month, count }))
  }, [users])

  const topBookmarked = useMemo(() => {
    const countMap = {}
    users.forEach((u) => {
      (u.bookmarks || []).forEach((b) => {
        countMap[b] = (countMap[b] || 0) + 1
      })
    })
    const arr = Object.entries(countMap)
      .map(([shlokId, count]) => ({ shlokId, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10)
    return arr
  }, [users])

  const themeCounts = useMemo(() => {
    return Object.entries(
      shloks.reduce((acc, s) => {
        const t = s.theme || 'Unknown'
        acc[t] = (acc[t] || 0) + 1
        return acc
      }, {})
    ).map(([name, value]) => ({ name, value }))
  }, [shloks])

  const chapterCounts = useMemo(() => {
    return Object.entries(
      shloks.reduce((acc, s) => {
        const c = s.chapter || 'Unknown'
        acc[c] = (acc[c] || 0) + 1
        return acc
      }, {})
    ).map(([chapter, count]) => ({ chapter, count }))
  }, [shloks])

  return (
    <div className="space-y-6">
      <div className="card p-4">
        <h3 className="font-semibold mb-3">User Growth per Month</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={growth}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#157fc3" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Removed: Shloks by Theme and Shloks by Chapter sections as requested */}

      <div className="card p-4">
        <h3 className="font-semibold mb-3">Top Bookmarked Shloks</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Shlok ID</th>
              <th>Bookmarks</th>
            </tr>
          </thead>
          <tbody>
            {topBookmarked.map((row) => (
              <tr key={row.shlokId}>
                <td>{row.shlokId}</td>
                <td>{row.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
