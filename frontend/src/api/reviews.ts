import { z } from 'zod'
import { claimSchema } from './claims'
import { apiMutation, apiRequest } from './client'
import { documentSchema,pageSchema } from './documents'
import { verificationSchema } from './verification'
export const reviewSchema=z.object({document:documentSchema,pages:z.array(pageSchema),claims:z.array(claimSchema),verifications:z.array(verificationSchema)})
export const summarySchema=z.object({document_id:z.string(),document_name:z.string(),upload_date:z.string(),claim_count:z.number(),supported_count:z.number(),contradicted_count:z.number(),not_found_count:z.number(),needs_review_count:z.number(),last_updated:z.string()})
export const listReviews=()=>apiRequest('/reviews',z.array(summarySchema))
export const getReview=(id:string)=>apiRequest(`/reviews/${id}`,reviewSchema)
export const loadSample=(id:string)=>apiMutation(`/samples/${id}/load`,reviewSchema)

