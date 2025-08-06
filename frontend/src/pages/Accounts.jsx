import AccountManager from '../components/AccountManager'

export default function Accounts({ token }) {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Account Management</h1>
      <AccountManager token={token} />
    </div>
  )
}
