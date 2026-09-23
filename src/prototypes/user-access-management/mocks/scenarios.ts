import { MOCK_USERS, type MockUser } from './users'

export type UamScenarioId =
  | 'default'
  | 'search'
  | 'filtered'
  | 'empty'
  | 'loading'
  | 'error'
  | 'selected'
  | 'multi'
  | 'viewer'
  | 'long'

export type UamScenario = {
  id: UamScenarioId
  label: string
  loadState: 'loaded' | 'loading' | 'error'
  role: 'admin' | 'viewer'
  /** Seed search / filters when scenario loads */
  initialQuery: string
  initialRoleFilter: string
  initialStatusFilter: string
  /** Preselected user ids */
  initialSelectedIds: string[]
  /** Override user list (e.g. empty) */
  users: MockUser[] | null
}

export const uamScenarios: Record<UamScenarioId, UamScenario> = {
  default: {
    id: 'default',
    label: 'Default',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  search: {
    id: 'search',
    label: 'Search',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: 'jordan',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  filtered: {
    id: 'filtered',
    label: 'Filtered',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'Editor',
    initialStatusFilter: 'Active',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  empty: {
    id: 'empty',
    label: 'No results',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: 'zzznomatch',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  loading: {
    id: 'loading',
    label: 'Loading',
    loadState: 'loading',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  error: {
    id: 'error',
    label: 'Error',
    loadState: 'error',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  selected: {
    id: 'selected',
    label: 'Selected',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: ['u-02'],
    users: MOCK_USERS,
  },
  multi: {
    id: 'multi',
    label: 'Multi-select',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: ['u-01', 'u-02', 'u-07'],
    users: MOCK_USERS,
  },
  viewer: {
    id: 'viewer',
    label: 'Viewer',
    loadState: 'loaded',
    role: 'viewer',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
  long: {
    id: 'long',
    label: 'Long content',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: 'montgomery',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    users: MOCK_USERS,
  },
}

export const UAM_SCENARIO_IDS = Object.keys(uamScenarios) as UamScenarioId[]

export function parseUamScenario(value: string | null | undefined): UamScenarioId {
  if (value && value in uamScenarios) return value as UamScenarioId
  return 'default'
}

export function getUamScenario(id: UamScenarioId): UamScenario {
  return uamScenarios[id]
}
