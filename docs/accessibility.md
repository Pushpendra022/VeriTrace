# Accessibility and responsive verification

Phase 11 includes semantic landmarks, a keyboard-visible skip link, labeled controls, live service and upload status, visible focus rings, text labels accompanying verdict colors, reduced-motion handling, responsive stacked workspace layout, and an interface-level error boundary.

Automated component tests cover upload keyboard controls, service startup announcements, exact evidence markup, document page controls, and result content. The production build uses strict TypeScript. Desktop and narrow layouts avoid fixed content widths; below 760 px the claim and document panes stack, result columns collapse, history reduces to essential fields, and navigation becomes horizontally scrollable.

Before a public release, run browser accessibility tooling against `/`, `/history`, `/how-it-works`, and a populated `/reviews/{id}` route at 320, 768, 1024, and 1440 CSS pixels. Manual checks should cover keyboard-only upload, claim editing, evidence navigation, 200% zoom, screen-reader status announcements, and reduced motion.

