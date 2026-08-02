import { useMutation, useQuery } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { createClaim, deleteClaim, extractClaims, updateClaim } from '../api/claims'
import { getReview } from '../api/reviews'
import { verifyClaim, verifyClaims } from '../api/verification'
import { ClaimPanel } from '../features/claim-editor/ClaimPanel'
import { DocumentViewer } from '../features/document-viewer/DocumentViewer'
import { VerificationResult } from '../features/verification/VerificationResult'
import { useReviewStore } from '../stores/reviewStore'

export function ReviewWorkspacePage() {
  const { documentId = '' } = useParams()
  const { review, selectedClaimId, selectedVerification, setReview, selectClaim, setVerification } = useReviewStore()
  const [message, setMessage] = useState('')
  const query = useQuery({ queryKey: ['review', documentId], queryFn: () => getReview(documentId), enabled: !!documentId })
  useEffect(() => { if (query.data) setReview(query.data) }, [query.data, setReview])
  const mutation = useMutation({ mutationFn: (id: string) => verifyClaim(id), onSuccess: result => { setVerification(result); setMessage('') }, onError: error => setMessage(error.message) })

  if (query.isPending && review?.document.id !== documentId) return <div className="page loading-page" role="status"><span className="spinner" aria-hidden="true" /> Loading review and evidence…</div>
  if (query.isError) return <div className="page form-error">{query.error.message}</div>
  if (!review) return null
  const refresh = async () => setReview(await getReview(documentId))

  return <div className="workspace">
    <div className="workspace-title"><div><span className="section-label">Review workspace</span><h1>{review.document.original_filename}</h1></div><span>{review.document.page_count} page{review.document.page_count === 1 ? '' : 's'} · {review.document.character_count.toLocaleString()} characters</span></div>
    {message && <p className="form-error" role="alert">{message}</p>}
    <div className="workspace-grid" aria-busy={mutation.isPending}>
      <ClaimPanel claims={review.claims} verifications={review.verifications} selectedId={selectedClaimId} busy={mutation.isPending}
        onSelect={id => { selectClaim(id); const result = review.verifications.find(item => item.claim_id === id); if (result) setVerification(result) }}
        onCreate={async text => { await createClaim(documentId, { claim_text: text, category: 'general', importance: 'medium' }); await refresh() }}
        onEdit={async (id, text) => { await updateClaim(id, { claim_text: text }); await refresh() }}
        onDelete={async id => { await deleteClaim(id); await refresh() }}
        onExtract={async () => { try { await extractClaims(documentId); await refresh() } catch (error) { setMessage(error instanceof Error ? error.message : 'Extraction failed.') } }}
        onVerify={id => mutation.mutate(id)}
        onVerifySelected={async ids => { try { const results = await verifyClaims(documentId, ids); await refresh(); if (results[0]) setVerification(results[0]) } catch (error) { setMessage(error instanceof Error ? error.message : 'Selected verification failed.') } }}
        onVerifyAll={async () => { try { const results = await verifyClaims(documentId); await refresh(); if (results[0]) setVerification(results[0]) } catch (error) { setMessage(error instanceof Error ? error.message : 'Bulk verification failed.') } }} />
      <DocumentViewer pages={review.pages} result={selectedVerification} />
    </div>
    <VerificationResult result={selectedVerification} />
  </div>
}
