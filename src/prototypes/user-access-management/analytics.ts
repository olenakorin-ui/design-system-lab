export type UamAnalyticsEvent =
  | 'uam_viewed'
  | 'uam_search_changed'
  | 'uam_filter_changed'
  | 'uam_selection_changed'
  | 'uam_invite_started'
  | 'uam_invite_cancelled'
  | 'uam_invite_submitted'
  | 'uam_bulk_started'
  | 'uam_bulk_cancelled'
  | 'uam_bulk_confirmed'
  | 'uam_row_action'
  | 'uam_tab_changed'

export function trackUam(
  event: UamAnalyticsEvent,
  payload: Record<string, unknown> = {},
): void {
  if (typeof window !== 'undefined') {
    const detail = { event, ...payload, at: new Date().toISOString() }
    window.dispatchEvent(new CustomEvent('ds-experiment-analytics', { detail }))
    console.info('[analytics]', event, payload)
  }
}
