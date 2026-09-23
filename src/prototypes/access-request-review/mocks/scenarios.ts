import type {
  LoadState,
  RequestStatus,
  ReviewerRole,
} from '../components/AccessRequestReview'

export type AccessRequestScenarioId =
  | 'pending'
  | 'approved'
  | 'rejected'
  | 'viewer'
  | 'error'

export type AccessRequestScenario = {
  id: AccessRequestScenarioId
  label: string
  requestId: string
  initialStatus: RequestStatus
  role: ReviewerRole
  loadState: LoadState
  longNames: boolean
  accessLevelDefault: 'Viewer' | 'Editor' | 'Administrator'
  referenceTicket: string
  requestor: string
  department: string
  system: string
}

const baseIdentity = {
  requestId: 'AR-1048',
  accessLevelDefault: 'Administrator' as const,
  referenceTicket: 'SEC-2841',
  requestor: 'Alex Morgan',
  department: 'Product Operations',
  system: 'Analytics Workspace',
  longNames: false,
}

export const accessRequestScenarios: Record<
  AccessRequestScenarioId,
  AccessRequestScenario
> = {
  pending: {
    id: 'pending',
    label: 'Pending',
    ...baseIdentity,
    initialStatus: 'pending',
    role: 'reviewer',
    loadState: 'loaded',
  },
  approved: {
    id: 'approved',
    label: 'Approved',
    ...baseIdentity,
    initialStatus: 'approved',
    role: 'reviewer',
    loadState: 'loaded',
  },
  rejected: {
    id: 'rejected',
    label: 'Rejected',
    ...baseIdentity,
    initialStatus: 'rejected',
    role: 'reviewer',
    loadState: 'loaded',
  },
  viewer: {
    id: 'viewer',
    label: 'Viewer',
    ...baseIdentity,
    initialStatus: 'pending',
    role: 'viewer',
    loadState: 'loaded',
  },
  error: {
    id: 'error',
    label: 'Error',
    ...baseIdentity,
    initialStatus: 'pending',
    role: 'reviewer',
    loadState: 'error',
  },
}

export const ACCESS_REQUEST_SCENARIO_IDS = Object.keys(
  accessRequestScenarios,
) as AccessRequestScenarioId[]

export function parseAccessRequestScenario(
  value: string | null | undefined,
): AccessRequestScenarioId {
  if (value && value in accessRequestScenarios) {
    return value as AccessRequestScenarioId
  }
  return 'pending'
}

export function getAccessRequestScenario(
  id: AccessRequestScenarioId,
): AccessRequestScenario {
  return accessRequestScenarios[id]
}
