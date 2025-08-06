import React, { useState } from 'react'

export default function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  const search = async () => {
    const res = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(query)}`)
    const data = await res.json()
    setResults(data)
  }

  return (
    <div>
      <h2>Search Leaked Data</h2>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Email, keyword..." />
      <button onClick={search}>Search</button>
      <ul>
        {results.map((r, i) => (
          <li key={i}><code>{r.content}</code></li>
        ))}
      </ul>
    </div>
  )
}
