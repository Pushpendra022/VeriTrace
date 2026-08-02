import { History } from 'lucide-react'
import { useQuery,useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { deleteDocument } from '../api/documents'
import { listReviews } from '../api/reviews'

export function HistoryPage() {
  const client=useQueryClient();const reviews=useQuery({queryKey:['reviews'],queryFn:listReviews})
  return (
    <div className="page narrow-page">
      <div className="page-heading"><div><p className="eyebrow"><History size={16} /> Review history</p><h1>Previous reviews</h1></div></div>
      {reviews.isPending?<section className="empty-state"><p>Loading review history…</p></section>:reviews.isError?<section className="empty-state form-error"><p>{reviews.error.message}</p></section>:reviews.data.length===0?<section className="empty-state">
        <h2>No reviews yet</h2>
        <p>Completed document reviews will appear here with verdict counts, timestamps, and evidence links.</p>
      </section>:<div className="history-table"><div className="history-row history-head"><span>Document</span><span>Claims</span><span>Verdicts</span><span>Updated</span><span/></div>{reviews.data.map(review=><div className="history-row" key={review.document_id}><div><Link to={`/reviews/${review.document_id}`}>{review.document_name}</Link><small>{new Date(review.upload_date).toLocaleDateString()}</small></div><span>{review.claim_count}</span><div className="summary-counts"><span className="supported">{review.supported_count} S</span><span className="contradicted">{review.contradicted_count} C</span><span className="not-found">{review.not_found_count} N</span><span>{review.needs_review_count} R</span></div><span>{new Date(review.last_updated).toLocaleDateString()}</span><button className="text-button danger" onClick={async()=>{if(confirm('Delete this review and all evidence traces?')){await deleteDocument(review.document_id);await client.invalidateQueries({queryKey:['reviews']})}}}>Delete</button></div>)}</div>}
    </div>
  )
}
