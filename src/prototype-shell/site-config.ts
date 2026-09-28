/**
 * Public site configuration for Prototype Lab showcase.
 * Replace placeholder values before linking from portfolio / LinkedIn / CV.
 */

/** Production origin used for canonical + Open Graph. */
export const SITE_ORIGIN = 'https://design-system-lab-weld.vercel.app'

export const SITE_TITLE = 'Olena Korin — Prototype Lab'

export const SITE_DESCRIPTION =
  'Interactive B2B product design experiments exploring AI-ready design systems, reusable React components, and evidence-driven product prototyping.'

export const OG_TITLE = 'Prototype Lab — AI-Powered Product Design'

export const OG_DESCRIPTION =
  'Explore interactive B2B workflows built from a reusable Figma-to-code design system and validated through real product experiments.'

/** Replace with the final portfolio case-study URL when available. */
export const CASE_STUDY_HREF = '#case-study-placeholder'

/**
 * Social / portfolio links. Leave null until a real URL exists — do not invent.
 * Footer renders labels as text when null.
 */
export const SOCIAL_LINKS = {
  portfolio: null as string | null,
  linkedin: null as string | null,
  github: null as string | null,
} as const

export const AUTHOR_NAME = 'Olena Korin'
export const AUTHOR_ROLE = 'Product Designer'
