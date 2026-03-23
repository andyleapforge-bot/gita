import React from 'react'

export default function StatsCard({ title, value, icon }) {
  return (
    <div className="card p-4 flex items-center">
      <div className="text-2xl mr-3">{icon}</div>
      <div>
        <div className="text-sm text-gray-500">{title}</div>
        <div className="text-2xl font-bold">{value}</div>
      </div>
    </div>
  )
}
