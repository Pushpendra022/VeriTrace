const verdicts = [
  ['SUPPORTED', 'Every material part of the claim is directly supported.'],
  ['CONTRADICTED', 'The source addresses the claim but materially disagrees.'],
  ['NOT_FOUND', 'The source does not address the claim.'],
  ['NEEDS_REVIEW', 'Relevant evidence exists, but the conclusion is uncertain.'],
]

export function HowItWorksPage() {
  return (
    <div className="page narrow-page prose-page">
      <p className="eyebrow">Methodology and limitations</p>
      <h1>How VeriTrace works</h1>
      <p className="lede">VeriTrace retrieves focused source passages, asks a replaceable Gemini provider for structured analysis, then validates facts and exact quotes locally before returning a verdict.</p>
      <section><h2>Four explicit verdicts</h2><div className="definition-list">{verdicts.map(([name, description]) => <div key={name}><strong>{name}</strong><span>{description}</span></div>)}</div></section>
      <section><h2>Evidence before confidence</h2><p>Confidence summarizes evidence quality and system agreement. It does not guarantee correctness. Exact evidence, its page, and deterministic checks remain the primary audit trail.</p></section>
      <section><h2>Privacy and limits</h2><p>Original uploads are processed through secure temporary files and removed after extraction. OCR is not included in version one, and this public demonstration is not a substitute for professional review.</p></section>
    </div>
  )
}

