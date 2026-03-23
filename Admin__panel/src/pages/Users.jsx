import React, { useEffect, useState } from 'react'
import DataTable from '../components/DataTable'
import ConfirmDialog from '../components/ConfirmDialog'
import { listUsers, deleteUser } from '../services/userService'
import { formatDate } from '../utils/format'

export default function Users() {
  const [users, setUsers] = useState([])
  const [selected, setSelected] = useState(null)
  const [confirmOpen, setConfirmOpen] = useState(false)

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'dob', label: 'DOB', render: (v) => (v ? formatDate(v) : '-') },
    { key: 'bookmarks', label: 'Bookmarks', render: (v) => (Array.isArray(v) ? v.length : 0) },
    { key: 'createdAt', label: 'Created', render: (v) => (v ? formatDate(v) : '-') },
  ]

  async function refresh() {
    const u = await listUsers()
    setUsers(u)
  }

  useEffect(() => {
    refresh()
  }, [])

  async function onDelete() {
    if (!selected) return
    await deleteUser(selected.id)
    setConfirmOpen(false)
    setSelected(null)
    refresh()
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Users</h2>
        <button className="btn" onClick={refresh}>Refresh</button>
      </div>
      <DataTable columns={columns} data={users} onRowClick={setSelected} />
      {selected && (
        <div className="card p-4">
          <h3 className="font-semibold mb-2">User Details</h3>
          <pre className="bg-gray-100 p-3 rounded">{JSON.stringify(selected, null, 2)}</pre>
          <div className="flex justify-end gap-2 mt-3">
            <button className="btn" onClick={() => setSelected(null)}>Close</button>
            <button className="btn btn-error" onClick={() => setConfirmOpen(true)}>Delete</button>
          </div>
        </div>
      )}

      <ConfirmDialog
        open={confirmOpen}
        title="Delete User"
        message={`Delete user ${selected?.email}? This will remove their document.`}
        onCancel={() => setConfirmOpen(false)}
        onConfirm={onDelete}
      />
    </div>
  )
}
