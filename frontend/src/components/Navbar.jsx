import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between">
      <div className="space-x-4">
        <Link to="/">Patterns</Link>
        <Link to="/search">Search</Link>
        <Link to="/accounts">Accounts</Link>
      </div>
    </nav>
  )
}
