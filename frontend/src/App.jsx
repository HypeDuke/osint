import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Search from './pages/Search'
import Accounts from './pages/Accounts'
import Login from './components/Login'
import { useState } from 'react'

function App() {
  const [token, setToken] = useState(null)

  if (!token) return <Login onLogin={setToken} />

  return (
    <Router>
      <Navbar />
      <div className="p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/accounts" element={<Accounts token={token} />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
