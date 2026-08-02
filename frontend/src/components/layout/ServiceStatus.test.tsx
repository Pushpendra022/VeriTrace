import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ServiceStatus } from './ServiceStatus'

describe('ServiceStatus',()=>{it('announces service startup details',()=>{vi.stubGlobal('fetch',vi.fn(()=>new Promise(()=>{})));render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><ServiceStatus/></QueryClientProvider>);expect(screen.getByRole('status')).toHaveTextContent('Starting service');expect(screen.getByText(/first visit may take 40–60 seconds/i)).toBeInTheDocument();vi.unstubAllGlobals()})})
