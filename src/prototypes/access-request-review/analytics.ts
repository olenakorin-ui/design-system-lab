export type AccessRequestAnalyticsEvent =
  | 'access_request_viewed'
  | 'access_request_tab_changed'
  | 'access_level_changed'
  | 'review_confirmation_checked'
  | 'decision_started'
  | 'decision_cancelled'
  | 'request_approved'
  | 'request_rejected'

export type AnalyticsPayload = Record<string, string | boolean | number | undefined>

/**
 * Experiment stub — replace with product analytics later.
 * Events are documented in docs/experiments/access-request-review-v0.1.md
 */
export function trackAccessRequest(
  event: AccessRequestAnalyticsEvent,
  payload: AnalyticsPayload = {},
) {
  if (typeof window !== 'undefined') {
    const detail = { event, ...payload, at: new Date().toISOString() }
    window.dispatchEvent(new CustomEvent('ds-experiment-analytics', { detail }))
    console.info('[analytics]', event, payload)
  }
}
