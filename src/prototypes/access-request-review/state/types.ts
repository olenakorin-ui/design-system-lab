/**
 * Local prototype state shape.
 * Designed so a later localStorage adapter can persist without changing page APIs.
 */
export type AccessRequestUiState = {
  accessLevel: 'Viewer' | 'Editor' | 'Administrator'
  referenceTicket: string
  confirmed: boolean
  status: 'pending' | 'approved' | 'rejected'
  feedback: string | null
}

export const ACCESS_REQUEST_STORAGE_KEY = 'prototype:access-request-review:v1'
