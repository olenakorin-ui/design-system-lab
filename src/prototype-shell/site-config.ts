/**
 * Public site configuration for Prototype Lab showcase.
 *
 * Set real absolute URLs when available. Leave null to hide the corresponding
 * public CTA/link — never ship hash placeholders or invented URLs.
 */

/** Production origin used for canonical + Open Graph. */
export const SITE_ORIGIN = 'https://design-system-lab-weld.vercel.app'

export const SITE_TITLE = 'Olena Korin — Prototype Lab'

export const SITE_DESCRIPTION =
  'Interactive B2B product design experiments exploring AI-ready design systems, reusable React components, and evidence-driven product prototyping.'

export const OG_TITLE = 'Prototype Lab — AI-Powered Product Design'

export const OG_DESCRIPTION =
  'Explore interactive B2B workflows built from a reusable Figma-to-code design system and validated through real product experiments.'

/**
 * Absolute URL to the portfolio case study.
 * null → hide “Read the case study” CTA (do not use hash placeholders).
 */
export const CASE_STUDY_HREF: string | null = null

/**
 * Social / portfolio links. null → omit from footer (do not invent URLs).
 */
export const SOCIAL_LINKS = {
  portfolio: null as string | null,
  linkedin: null as string | null,
  github: null as string | null,
} as const

export const AUTHOR_NAME = 'Olena Korin'
export const AUTHOR_ROLE = 'Product Designer'

/**
 * Open Graph image path (served from /public).
 * Current fallback: SVG placeholder. Final 1200×630 raster is non-blocking
 * public polish — metadata already points here; replace file when ready.
 */
export const OG_IMAGE_PATH = '/og-image.svg'

/** True when a real public href is configured (absolute http(s) URL). */
export function hasPublicHref(href: string | null | undefined): href is string {
  if (!href) return false
  const trimmed = href.trim()
  if (!trimmed) return false
  return /^https?:\/\//i.test(trimmed)
}
