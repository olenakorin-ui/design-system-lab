/**
 * Product analytics for User Access Management (Prototype Lab).
 *
 * Events are dispatched as `ds-experiment-analytics` CustomEvents and logged
 * to the console for experiment measurement. They are **not** sent as Vercel
 * Web Analytics custom events (Hobby plan does not support custom events).
 */

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
  /** Directory page index changed via Pagination */
  | 'user_directory_page_changed'
  /** Empty-state primary CTA (Invite user / Clear filters) */
  | 'user_directory_empty_action_clicked'
  /** Filters/search/tab reset from empty-state Clear filters */
  | 'user_directory_filters_cleared'

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
