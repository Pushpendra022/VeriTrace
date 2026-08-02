import { Component, type ErrorInfo, type ReactNode } from 'react'

interface Props { children: ReactNode }
interface State { failed: boolean }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { failed: false }
  static getDerivedStateFromError(): State { return { failed: true } }
  componentDidCatch(error: Error, info: ErrorInfo) { console.error('VeriTrace interface error', error, info.componentStack) }
  render() {
    if (this.state.failed) return <main id="main-content" className="page"><section className="empty-state" role="alert"><h1>Something went wrong</h1><p>The interface could not display this view. Your persisted review data has not been removed.</p><button className="button button--primary" onClick={() => window.location.assign('/')}>Return to new review</button></section></main>
    return this.props.children
  }
}
