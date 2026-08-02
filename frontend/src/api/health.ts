import { z } from 'zod'
import { apiRequest } from './client'

export const healthSchema = z.object({
  status: z.literal('ok'),
  database: z.literal('connected'),
  llm_provider: z.enum(['gemini', 'mock']),
})

export type Health = z.infer<typeof healthSchema>

export const getHealth = (signal?: AbortSignal) => apiRequest('/health', healthSchema, signal)

