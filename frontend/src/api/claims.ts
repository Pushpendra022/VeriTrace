import { z } from 'zod'
import type { Claim } from '../types'
import { apiBase, apiMutation, apiRequest } from './client'

export const claimSchema=z.object({id:z.string(),document_id:z.string(),claim_text:z.string(),category:z.string(),importance:z.enum(['low','medium','high']),source_type:z.string(),status:z.string(),created_at:z.string(),updated_at:z.string()})
export const listClaims=(documentId:string)=>apiRequest(`/documents/${documentId}/claims`,z.array(claimSchema))
export const createClaim=(documentId:string,payload:{claim_text:string;category:string;importance:string})=>apiMutation(`/documents/${documentId}/claims`,claimSchema,'POST',payload) as Promise<Claim>
export const updateClaim=(claimId:string,payload:{claim_text:string})=>apiMutation(`/claims/${claimId}`,claimSchema,'PATCH',payload) as Promise<Claim>
export const extractClaims=(documentId:string)=>apiMutation(`/documents/${documentId}/claims/extract`,z.array(claimSchema))
export const deleteClaim=(claimId:string)=>fetch(`${apiBase}/claims/${claimId}`,{method:'DELETE'}).then(response=>{if(!response.ok)throw new Error('Could not delete the claim.')})

