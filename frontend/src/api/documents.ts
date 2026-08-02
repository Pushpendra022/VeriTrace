import { z } from 'zod'
import type { Review } from '../types'
import { apiBase } from './client'

export const pageSchema = z.object({id:z.string(),document_id:z.string(),page_number:z.number(),text:z.string(),start_char:z.number(),end_char:z.number()})
export const documentSchema = z.object({id:z.string(),filename:z.string(),original_filename:z.string(),mime_type:z.string(),file_size:z.number(),status:z.string(),page_count:z.number(),character_count:z.number(),created_at:z.string(),updated_at:z.string()})

export function uploadDocument(file: File, onProgress:(percent:number, stage:'uploading'|'extracting')=>void): Promise<Review> {
  return new Promise((resolve,reject)=>{
    const xhr=new XMLHttpRequest(); const body=new FormData(); body.append('file',file)
    xhr.open('POST',`${apiBase}/documents`)
    xhr.upload.onprogress=(event)=>{if(event.lengthComputable){const percent=Math.round(event.loaded/event.total*100);onProgress(percent,percent===100?'extracting':'uploading')}}
    xhr.onerror=()=>reject(new Error('Network error while uploading the document.'))
    xhr.onload=()=>{let payload:unknown;try{payload=JSON.parse(xhr.responseText)}catch{reject(new Error('The service returned an invalid response.'));return}if(xhr.status<200||xhr.status>=300){const error=payload as {error?:{message?:string}};reject(new Error(error.error?.message??'Upload failed.'));return}const parsed=documentSchema.extend({pages:z.array(pageSchema)}).parse(payload);resolve({document:parsed,pages:parsed.pages,claims:[],verifications:[]})}
    xhr.send(body)
  })
}
export const deleteDocument=(id:string)=>fetch(`${apiBase}/documents/${id}`,{method:'DELETE'}).then(response=>{if(!response.ok)throw new Error('Could not delete this review.')})
