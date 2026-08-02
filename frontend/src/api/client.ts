import { z } from 'zod'

export const apiBase = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api').replace(/\/$/, '')

const errorSchema = z.object({
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.record(z.string(), z.unknown()).optional(),
  }),
})

export class ApiError extends Error {
  constructor(
    message: string,
    readonly code: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export async function apiRequest<T>(path: string, schema: z.ZodType<T>, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, { headers: { Accept: 'application/json' }, signal })
  const body: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    const parsed = errorSchema.safeParse(body)
    throw new ApiError(parsed.success ? parsed.data.error.message : 'The service is unavailable.', parsed.success ? parsed.data.error.code : 'NETWORK_ERROR', response.status)
  }
  return schema.parse(body)
}

export async function apiMutation<T>(path:string, schema:z.ZodType<T>, method:'POST'|'PATCH'='POST', body?:unknown):Promise<T>{
  const response=await fetch(`${apiBase}${path}`,{method,headers:{Accept:'application/json','Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)})
  const data:unknown=await response.json().catch(()=>null)
  if(!response.ok){const parsed=errorSchema.safeParse(data);throw new ApiError(parsed.success?parsed.data.error.message:'The request failed.',parsed.success?parsed.data.error.code:'REQUEST_ERROR',response.status)}
  return schema.parse(data)
}

