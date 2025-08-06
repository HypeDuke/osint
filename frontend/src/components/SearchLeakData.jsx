import { useState } from 'react'

export default function SearchLeakedData() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  const search = async () => {
    const res = await fetch(`/search/?keyword=${encodeURIComponent(query)}`)
    const data = await res.json()
    setResults(data)
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Search Leaked Data</h2>
      <input
        className="border p-2 w-full"
        placeholder="Enter keyword/email..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={search} className="bg-blue-500 text-white px-4 py-2 rounded">Search</button>

      <ul className="mt-4 space-y-2">
        {results.map((r, i) => (
          <li key={i} className="bg-gray-100 p-2 rounded">{r.content}</li>
        ))}
      </ul>
    </div>
  )
}
