import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// App.jsx
import React, { useState } from 'react'
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom'
import PatternAdmin from './PatternAdmin'
import Search from './Search'
import AccountManager from './AccountManager'
import Login from './Login'

function App() {
  const [token, setToken] = useState(null)

  if (!token) {
    return <Login onLogin={setToken} />
  }

  return (
    <Router>
      <nav>
        <Link to="/">Patterns</Link> | <Link to="/search">Search</Link> | <Link to="/accounts">Accounts</Link>
      </nav>
      <Routes>
        <Route path="/" element={<PatternAdmin />} />
        <Route path="/search" element={<Search />} />
        <Route path="/accounts" element={<AccountManager token={token} />} />
      </Routes>
    </Router>
  )
}

export default App