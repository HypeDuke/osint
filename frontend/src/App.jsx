import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import SearchLeakedData from './components/SearchLeakedData'
import PatternAdmin from './components/PatternAdmin'
import AccountManager from './components/AccountManager'
import Login from './components/Login'
import { useState } from 'react'

function App() {
  const [token, setToken] = useState(null)

  if (!token) return <Login onLogin={setToken} />

  return (
    <Router>
      <Navbar />
      <div className="p-6">
        <Routes>
          <Route path="/" element={<PatternAdmin />} />
          <Route path="/search" element={<SearchLeakedData />} />
          <Route path="/accounts" element={<AccountManager token={token} />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
