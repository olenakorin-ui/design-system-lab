export type UamUiState = {
  query: string
  roleFilter: string
  statusFilter: string
  selectedIds: string[]
  tab: 'all' | 'needs-attention'
}

export const UAM_STORAGE_KEY = 'prototype:user-access-management:v1'
