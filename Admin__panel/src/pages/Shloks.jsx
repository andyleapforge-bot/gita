import React, { useEffect, useMemo, useState } from 'react'
import DataTable from '../components/DataTable'
import FilterBar from '../components/FilterBar'
import Modal from '../components/Modal'
import ConfirmDialog from '../components/ConfirmDialog'
import { listShloks, addShlok, updateShlok, deleteShlok } from '../services/shlokService'

export default function Shloks() {
  const [rows, setRows] = useState([])
  const [selectedThemes, setSelectedThemes] = useState([])
  const [selectedChapters, setSelectedChapters] = useState([])
  const [editOpen, setEditOpen] = useState(false)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [current, setCurrent] = useState(null)
  const empty = { id: '', chapter: '', theme: '', devanagari: '', translation: '', meaning: '' }

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'chapter', label: 'Chapter' },
    { key: 'theme', label: 'Theme' },
    { key: 'devanagari', label: 'Devanagari' },
    { key: 'translation', label: 'Translation' },
    { key: 'meaning', label: 'Meaning' },
  ]

  async function refresh() {
    const list = await listShloks()
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
    if (id) await updateShlok(id, rest)
    else await addShlok(rest)
    setEditOpen(false)
    setCurrent(null)
    refresh()
  }

  async function onDelete() {
    if (!current?.id) return
    await deleteShlok(current.id)
    setConfirmOpen(false)
    setCurrent(null)
    refresh()
  }

  function toggleTheme(theme) {
    setSelectedThemes((prev) => (
      prev.includes(theme) ? prev.filter((t) => t !== theme) : [...prev, theme]
    ))
  }

  function toggleChapter(ch) {
    setSelectedChapters((prev) => (
      prev.includes(ch) ? prev.filter((c) => c !== ch) : [...prev, ch]
    ))
  }

  const themeOptions = useMemo(() => {
    const set = new Set(rows.map((r) => r.theme).filter(Boolean))
    return Array.from(set).map((t) => ({ label: t, value: t }))
  }, [rows])

  const chapterOptions = useMemo(() => {
    const set = new Set(rows.map((r) => String(r.chapter)).filter(Boolean))
    return Array.from(set).map((c) => ({ label: `Chapter ${c}`, value: c }))
  }, [rows])

  const filteredRows = useMemo(() => {
    return rows.filter((r) => {
      const themeOk = selectedThemes.length === 0 || selectedThemes.includes(r.theme)
      const chapVal = r.chapter != null ? String(r.chapter) : ''
      const chapterOk = selectedChapters.length === 0 || selectedChapters.includes(chapVal)
      return themeOk && chapterOk
    })
  }, [rows, selectedThemes, selectedChapters])

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Shloks</h2>
        <button className="btn-gold" onClick={openNew}>Add Shlok</button>
      </div>
      <div className="flex items-center gap-4">
        <div>
          <p className="text-sm font-medium mb-1">Filter by Theme</p>
          <FilterBar options={themeOptions} selected={selectedThemes} onToggle={toggleTheme} />
        </div>
        <div>
          <p className="text-sm font-medium mb-1">Filter by Chapter</p>
          <FilterBar options={chapterOptions} selected={selectedChapters} onToggle={toggleChapter} />
        </div>
      </div>

      <DataTable columns={columns} data={filteredRows} onRowClick={openEdit} />

      <Modal open={editOpen} title={current?.id ? 'Edit Shlok' : 'Add Shlok'} onClose={() => setEditOpen(false)}>
        <div className="grid grid-cols-1 gap-3">
          {['chapter','theme','devanagari','translation','meaning'].map((k) => (
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
        title="Delete Shlok"
        message={`Delete shlok ${current?.id}?`}
        onCancel={() => setConfirmOpen(false)}
        onConfirm={onDelete}
      />
    </div>
  )
}
