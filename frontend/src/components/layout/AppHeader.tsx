import { FilePlus2 } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { BrandMark } from './BrandMark'
import { ServiceStatus } from './ServiceStatus'

const navClass = ({ isActive }: { isActive: boolean }) => `nav-link${isActive ? ' nav-link--active' : ''}`

export function AppHeader() {
  return (
    <header className="app-header">
      <div className="header-inner">
        <NavLink to="/" className="brand inline-flex" aria-label="VeriTrace home">
          <BrandMark />
          <span>VeriTrace</span>
        </NavLink>
        <nav aria-label="Primary navigation">
          <NavLink to="/" className={navClass}><FilePlus2 size={15} /> New Review</NavLink>
          <NavLink to="/history" className={navClass}>History</NavLink>
          <NavLink to="/how-it-works" className={navClass}>How It Works</NavLink>
        </nav>
        <ServiceStatus />
      </div>
    </header>
  )
}
