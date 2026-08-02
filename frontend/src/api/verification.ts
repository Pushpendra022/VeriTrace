import { z } from 'zod'
import { apiMutation } from './client'

export const verificationSchema=z.object({verification_id:z.string(),claim_id:z.string(),verdict:z.enum(['SUPPORTED','CONTRADICTED','NOT_FOUND','NEEDS_REVIEW']),confidence:z.number(),quote:z.string(),explanation:z.string(),source:z.object({document_id:z.string(),document_name:z.string(),page_number:z.number().nullable(),chunk_id:z.string().nullable(),start_char:z.number().nullable(),end_char:z.number().nullable()}),checks:z.object({quote_verified:z.boolean(),numbers_consistent:z.boolean(),percentages_consistent:z.boolean(),dates_consistent:z.boolean(),currency_consistent:z.boolean()}),metrics:z.object({latency_ms:z.number(),chunks_searched:z.number(),chunks_retrieved:z.number(),context_characters:z.number(),provider:z.string(),model:z.string(),prompt_version:z.string()}),created_at:z.string()})
export const verifyClaim=(id:string)=>apiMutation(`/claims/${id}/verify`,verificationSchema)
export const verifyClaims=(documentId:string,claimIds?:string[])=>apiMutation(`/documents/${documentId}/verify`,z.array(verificationSchema),'POST',{claim_ids:claimIds})

