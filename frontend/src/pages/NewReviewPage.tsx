import { FileSearch, Highlighter, ListChecks, LockKeyhole, SearchCheck } from 'lucide-react'
import { Link } from 'react-router-dom'
import { UploadPanel } from '../features/upload/UploadPanel'

export function NewReviewPage() {
  return (
    <div className="page landing-page">
      <section className="intro" aria-labelledby="page-title">
        <p className="eyebrow"><FileSearch size={16} /> Evidence verification workspace</p>
        <h1 id="page-title">Verify claims against source documents.</h1>
        <p className="lede">Upload a financial or business document, add a claim, and trace every verdict to exact source evidence.</p>
      </section>

      <UploadPanel />

      <div className="landing-support">
        <div className="privacy-note"><LockKeyhole size={16} /><span>Processed securely. Original files are removed after text extraction.</span></div>
        <Link className="text-link" to="/how-it-works">How verification works <span aria-hidden="true">→</span></Link>
      </div>

      <section className="workflow-summary" aria-label="Verification workflow">
        <div><SearchCheck size={18} /><span><strong>Focused retrieval</strong><small>Finds the most relevant source passages.</small></span></div>
        <div><ListChecks size={18} /><span><strong>Fact validation</strong><small>Checks numbers, dates, currencies, and units.</small></span></div>
        <div><Highlighter size={18} /><span><strong>Exact evidence</strong><small>Links every conclusion to a verified quote.</small></span></div>
      </section>
    </div>
  )
}
