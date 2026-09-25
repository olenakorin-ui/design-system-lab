import { MOCK_USERS, type MockUser } from './users'

/** Prototype page size for mocked client-side pagination (not a DS API). */
export const UAM_PAGE_SIZE = 5

export type UamScenarioId =
  | 'default'
  | 'search'
  | 'filtered'
  | 'empty'
  | 'search-no-results'
  | 'loading'
  | 'error'
  | 'selected'
  | 'multi'
  | 'multi-page-selection'
  | 'page-first'
  | 'page-middle'
  | 'page-last'
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
  /** Preselected user ids (persist across pages) */
  initialSelectedIds: string[]
  /** 1-based page seed; clamped when invalid after filter */
  initialPage: number
  /** Override user list (e.g. empty directory) */
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
    initialPage: 1,
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
    initialPage: 1,
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
    initialPage: 1,
    users: MOCK_USERS,
  },
  empty: {
    id: 'empty',
    label: 'Empty',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    initialPage: 1,
    users: [],
  },
  'search-no-results': {
    id: 'search-no-results',
    label: 'No results',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: 'zzznomatch',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    initialPage: 1,
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
    initialPage: 1,
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
    initialPage: 1,
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
    initialPage: 1,
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
    initialPage: 1,
    users: MOCK_USERS,
  },
  'multi-page-selection': {
    id: 'multi-page-selection',
    label: 'Multi-page select',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    // Page 1: u-01, u-02; Page 2: u-06 → bulk count 3
    initialSelectedIds: ['u-01', 'u-02', 'u-06'],
    initialPage: 1,
    users: MOCK_USERS,
  },
  'page-first': {
    id: 'page-first',
    label: 'Page 1',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    initialPage: 1,
    users: MOCK_USERS,
  },
  'page-middle': {
    id: 'page-middle',
    label: 'Page 2',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    initialPage: 2,
    users: MOCK_USERS,
  },
  'page-last': {
    id: 'page-last',
    label: 'Page last',
    loadState: 'loaded',
    role: 'admin',
    initialQuery: '',
    initialRoleFilter: 'All roles',
    initialStatusFilter: 'All statuses',
    initialSelectedIds: [],
    initialPage: 99,
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
    initialPage: 1,
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
    initialPage: 1,
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
