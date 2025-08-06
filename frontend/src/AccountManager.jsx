import React, { useState, useEffect } from 'react'

export default function AccountManager({ token }) {
  const [users, setUsers] = useState([])
  const [newUser, setNewUser] = useState('')
  const [newPass, setNewPass] = useState('')

  const loadUsers = async () => {
    const res = await fetch('http://localhost:8000/users', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    setUsers(data)
  }

  const addUser = async () => {
    await fetch('http://localhost:8000/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ username: newUser, password: newPass })
    })
    setNewUser('')
    setNewPass('')
    loadUsers()
  }

  const deleteUser = async (username) => {
    await fetch(`http://localhost:8000/users/${username}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    loadUsers()
  }

  useEffect(() => { loadUsers() }, [])

  return (
    <div>
      <h2>Account Management</h2>
      <input placeholder="Username" value={newUser} onChange={(e) => setNewUser(e.target.value)} />
      <input type="password" placeholder="Password" value={newPass} onChange={(e) => setNewPass(e.target.value)} />
      <button onClick={addUser}>Add</button>
      <ul>
        {users.map((u, i) => (
          <li key={i}>{u} <button onClick={() => deleteUser(u)}>Delete</button></li>
        ))}
      </ul>
    </div>
  )
}
