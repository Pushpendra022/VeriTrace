import { create } from 'zustand'
import type { Review, Verification } from '../types'
interface ReviewState{review:Review|null;selectedClaimId:string|null;selectedVerification:Verification|null;setReview:(review:Review)=>void;selectClaim:(id:string)=>void;setVerification:(result:Verification)=>void}
export const useReviewStore=create<ReviewState>((set)=>({review:null,selectedClaimId:null,selectedVerification:null,setReview:(review)=>set({review,selectedClaimId:review.claims[0]?.id??null,selectedVerification:review.verifications[0]??null}),selectClaim:(selectedClaimId)=>set({selectedClaimId}),setVerification:(result)=>set(state=>({selectedVerification:result,review:state.review?{...state.review,verifications:[...state.review.verifications.filter(item=>item.claim_id!==result.claim_id),result]}:null}))}))

