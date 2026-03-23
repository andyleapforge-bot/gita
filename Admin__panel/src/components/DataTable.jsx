import React from 'react'

export default function DataTable({ columns = [], data = [], onRowClick }) {
  return (
    <div className="overflow-x-auto card">
      <table className="table">
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c.key}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id || row.uid} onClick={() => onRowClick?.(row)} className="cursor-pointer">
              {columns.map((c) => (
                <td key={c.key}>{c.render ? c.render(row[c.key], row) : row[c.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
