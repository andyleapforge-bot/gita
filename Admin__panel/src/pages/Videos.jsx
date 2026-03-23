import React, { useEffect, useState } from 'react'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import ConfirmDialog from '../components/ConfirmDialog'
import { listVideos, addVideo, updateVideo, deleteVideo } from '../services/videoService'

export default function Videos() {
  const [rows, setRows] = useState([])
  const [editOpen, setEditOpen] = useState(false)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [current, setCurrent] = useState(null)
  const empty = { id: '', shlokId: '', youtubeUrl: '', title: '', description: '' }

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'shlokId', label: 'Shlok ID' },
    { key: 'youtubeUrl', label: 'YouTube URL' },
    { key: 'title', label: 'Title' },
    { key: 'description', label: 'Description' },
  ]

  async function refresh() {
    const list = await listVideos()
    setRows(list)
  }

  useEffect(() => { refresh() }, [])

  function openNew() {
    setCurrent({ ...empty })
    setEditOpen(true)
  }

  function openEdit(row) {
    setCurrent({ ...row })
    setEditOpen(true)
  }

  async function save() {
    const { id, ...rest } = current
    if (id) await updateVideo(id, rest)
    else await addVideo(rest)
    setEditOpen(false)
    setCurrent(null)
    refresh()
  }

  async function onDelete() {
    if (!current?.id) return
    await deleteVideo(current.id)
    setConfirmOpen(false)
    setCurrent(null)
    refresh()
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Videos</h2>
        <button className="btn-gold" onClick={openNew}>Add Video</button>
      </div>
      <DataTable columns={columns} data={rows} onRowClick={openEdit} />

      <Modal open={editOpen} title={current?.id ? 'Edit Video' : 'Add Video'} onClose={() => setEditOpen(false)}>
        <div className="grid grid-cols-1 gap-3">
          {['shlokId','youtubeUrl','title','description'].map((k) => (
            <input key={k} className="input input-bordered w-full" placeholder={k}
              value={current?.[k] || ''}
              onChange={(e) => setCurrent({ ...current, [k]: e.target.value })} />
          ))}
          <div className="flex justify-end gap-2">
            {current?.id && (
              <button className="btn btn-error" onClick={() => setConfirmOpen(true)}>Delete</button>
            )}
            <button className="btn" onClick={() => setEditOpen(false)}>Cancel</button>
            <button className="btn-gold" onClick={save}>Save</button>
          </div>
        </div>
      </Modal>

      <ConfirmDialog
        open={confirmOpen}
        title="Delete Video"
        message={`Delete video ${current?.id}?`}
        onCancel={() => setConfirmOpen(false)}
        onConfirm={onDelete}
      />
    </div>
  )
}
