import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return <div className="page narrow-page empty-state"><h1>Page not found</h1><p>The requested VeriTrace page does not exist.</p><Link className="text-link" to="/">Start a new review</Link></div>
}

