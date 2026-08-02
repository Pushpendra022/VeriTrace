import { Outlet } from 'react-router-dom'
import { AppFooter } from '../components/layout/AppFooter'
import { AppHeader } from '../components/layout/AppHeader'

export function AppLayout() {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <AppHeader />
      <main id="main-content"><Outlet /></main>
      <AppFooter />
    </div>
  )
}
