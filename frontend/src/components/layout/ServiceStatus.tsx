import { useQuery } from '@tanstack/react-query'
import { getHealth } from '../../api/health'

export function ServiceStatus() {
  const health = useQuery({
    queryKey: ['health'],
    queryFn: ({ signal }) => getHealth(signal),
    retry: 2,
    retryDelay: 1500,
    refetchInterval: 30_000,
  })

  const state = health.isPending ? 'starting' : health.isSuccess ? 'online' : 'unavailable'
  const label = state === 'starting' ? 'Starting service' : state === 'online' ? 'Online' : 'Unavailable'

  return (
    <span className={`service-status service-status--${state}`} role="status" aria-live="polite">
      <span className={`status-dot status-dot--${state}`} aria-hidden="true" />
      <span>{label}</span>
      {state === 'starting' && <span className="startup-note">First visit may take 40–60 seconds</span>}
      {state === 'unavailable' && <span className="service-detail">The verification service is unavailable. Check your connection and try again shortly.</span>}
    </span>
  )
}
