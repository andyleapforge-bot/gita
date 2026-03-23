import React from 'react'

export default function FilterBar({ options = [], selected = [], onToggle }) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((opt) => {
        const active = selected.includes(opt.value)
        return (
          <button
            key={opt.value}
            type="button"
            className={active ? 'btn btn-sm btn-primary' : 'btn btn-sm'}
            onClick={() => onToggle?.(opt.value)}
            aria-pressed={active}
          >
            {opt.label}
          </button>
        )
      })}
    </div>
  )
}
