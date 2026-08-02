export type Verdict = 'SUPPORTED' | 'CONTRADICTED' | 'NOT_FOUND' | 'NEEDS_REVIEW'
export interface DocumentInfo { id:string; filename:string; original_filename:string; mime_type:string; file_size:number; status:string; page_count:number; character_count:number; created_at:string; updated_at:string }
export interface DocumentPage { id:string; document_id:string; page_number:number; text:string; start_char:number; end_char:number }
export interface Claim { id:string; document_id:string; claim_text:string; category:string; importance:'low'|'medium'|'high'; source_type:string; status:string; created_at:string; updated_at:string }
export interface Verification { verification_id:string; claim_id:string; verdict:Verdict; confidence:number; quote:string; explanation:string; source:{document_id:string;document_name:string;page_number:number|null;chunk_id:string|null;start_char:number|null;end_char:number|null}; checks:{quote_verified:boolean;numbers_consistent:boolean;percentages_consistent:boolean;dates_consistent:boolean;currency_consistent:boolean}; metrics:{latency_ms:number;chunks_searched:number;chunks_retrieved:number;context_characters:number;provider:string;model:string;prompt_version:string};created_at:string }
export interface Review { document:DocumentInfo; pages:DocumentPage[]; claims:Claim[]; verifications:Verification[] }
export interface ReviewSummary { document_id:string;document_name:string;upload_date:string;claim_count:number;supported_count:number;contradicted_count:number;not_found_count:number;needs_review_count:number;last_updated:string }

