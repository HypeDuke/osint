import React, { useState } from 'react'

export default function Login({ onLogin }) {
  const [username, setUser] = useState('')
  const [password, setPass] = useState('')

  const handleLogin = async () => {
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (res.ok) {
      const data = await res.json()
      onLogin(data.token)
    } else {
      alert('Login failed')
    }
  }

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Username" value={username} onChange={e => setUser(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPass(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  )
}
