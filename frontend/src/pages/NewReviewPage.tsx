import { FileSearch, LockKeyhole } from 'lucide-react'
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

      <div className="privacy-note"><LockKeyhole size={16} /><span>Uploaded documents are processed securely. Original files are removed after text extraction.</span></div>
      <Link className="text-link" to="/how-it-works">Learn how evidence verification works →</Link>
    </div>
  )
}
