import { useState, useEffect } from 'react'

export default function PatternAdmin() {
  const [patterns, setPatterns] = useState([])
  const [newPattern, setNewPattern] = useState('')

  const loadPatterns = async () => {
    const res = await fetch('/patterns/')
    const data = await res.json()
    setPatterns(data)
  }

  const addPattern = async () => {
    if (!newPattern) return
    const res = await fetch('/patterns/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pattern: newPattern })
    })
    if (res.ok) {
      setNewPattern('')
      loadPatterns()
    } else {
      const err = await res.json()
      alert(err.detail)
    }
  }

  const deletePattern = async (pattern) => {
    const res = await fetch('/patterns/', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pattern })
    })
    if (res.ok) {
      loadPatterns()
    } else {
      const err = await res.json()
      alert(err.detail)
    }
  }

  useEffect(() => { loadPatterns() }, [])

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Manage Patterns</h2>
      <div className="flex space-x-2">
        <input
          className="border p-2 flex-grow"
          placeholder="New Pattern Regex..."
          value={newPattern}
          onChange={(e) => setNewPattern(e.target.value)}
        />
        <button onClick={addPattern} className="bg-green-500 text-white px-4 py-2 rounded">Add</button>
      </div>

      <ul className="mt-4 space-y-2">
        {patterns.map((p) => (
          <li key={p.id} className="flex justify-between bg-gray-100 p-2 rounded">
            <span>{p.id}: {p.pattern}</span>
            <button onClick={() => deletePattern(p.pattern)} className="text-red-500">Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
