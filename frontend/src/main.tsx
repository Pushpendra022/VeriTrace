import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { App } from './App'
import './index.css'
import { ErrorBoundary } from './components/feedback/ErrorBoundary'

const queryClient = new QueryClient({ defaultOptions: { queries: { staleTime: 15_000 } } })

createRoot(document.getElementById('root')!).render(
  <StrictMode><ErrorBoundary><QueryClientProvider client={queryClient}><App /></QueryClientProvider></ErrorBoundary></StrictMode>,
)
