import { useQuery } from '@tanstack/react-query'
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
  const [activeAction, setActiveAction] = useState<{ key: string; label: string } | null>(null)
  const query = useQuery({ queryKey: ['review', documentId], queryFn: () => getReview(documentId), enabled: !!documentId })
  useEffect(() => { if (query.data) setReview(query.data) }, [query.data, setReview])

  if (query.isPending && review?.document.id !== documentId) return <div className="page loading-page" role="status"><span className="spinner" aria-hidden="true" /> Loading review and evidence…</div>
  if (query.isError) return <div className="page form-error">{query.error.message}</div>
  if (!review) return null
  const refresh = async () => setReview(await getReview(documentId))
  const runAction = async (key: string, label: string, action: () => Promise<void>) => {
    setActiveAction({ key, label }); setMessage('')
    try { await action() } catch (error) { setMessage(error instanceof Error ? error.message : `${label} failed. Please try again.`) } finally { setActiveAction(null) }
  }

  return <div className="workspace">
    <div className="workspace-title"><div><span className="section-label">Review workspace</span><h1>{review.document.original_filename}</h1></div><span>{review.document.page_count} page{review.document.page_count === 1 ? '' : 's'} · {review.document.character_count.toLocaleString()} characters</span></div>
    {message && <p className="form-error" role="alert">{message}</p>}
    {activeAction && <div className="operation-status" role="status" aria-live="polite"><span className="spinner spinner--small" aria-hidden="true" /><span><strong>{activeAction.label}</strong><small>Please wait—VeriTrace is processing your request.</small></span></div>}
    <div className="workspace-grid" aria-busy={!!activeAction}>
      <ClaimPanel claims={review.claims} verifications={review.verifications} selectedId={selectedClaimId} busy={!!activeAction} activeAction={activeAction?.key ?? null}
        onSelect={id => { selectClaim(id); const result = review.verifications.find(item => item.claim_id === id); if (result) setVerification(result) }}
        onCreate={text => runAction('create', 'Adding claim…', async () => { await createClaim(documentId, { claim_text: text, category: 'general', importance: 'medium' }); await refresh() })}
        onEdit={(id, text) => runAction(`edit:${id}`, 'Saving claim…', async () => { await updateClaim(id, { claim_text: text }); await refresh() })}
        onDelete={id => runAction(`delete:${id}`, 'Deleting claim…', async () => { await deleteClaim(id); await refresh() })}
        onExtract={() => runAction('extract', 'Extracting claims…', async () => { await extractClaims(documentId); await refresh() })}
        onVerify={id => runAction(`verify:${id}`, 'Verifying claim…', async () => { setVerification(await verifyClaim(id)) })}
        onVerifySelected={ids => runAction('verify-selected', 'Verifying selected claims…', async () => { const results = await verifyClaims(documentId, ids); await refresh(); if (results[0]) setVerification(results[0]) })}
        onVerifyAll={() => runAction('verify-all', 'Verifying all claims…', async () => { const results = await verifyClaims(documentId); await refresh(); if (results[0]) setVerification(results[0]) })} />
      <DocumentViewer pages={review.pages} result={selectedVerification} />
    </div>
    <VerificationResult result={selectedVerification} />
  </div>
}
