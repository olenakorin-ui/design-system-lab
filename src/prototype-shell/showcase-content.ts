export const showcaseMetrics = [
  { value: '2', label: 'Validated product workflows' },
  { value: '13', label: 'Reusable DS components' },
  { value: '0', label: 'Critical accessibility issues' },
  { value: 'v0.2', label: 'Evidence-driven DS release' },
] as const

export const systemPipeline = [
  'Figma',
  'Design tokens',
  'React components',
  'Storybook validation',
  'Interactive prototypes',
  'Production analytics',
  'Design system iteration',
] as const

export const feedbackLoop = [
  'Prototype need',
  'DS gap',
  'Component added',
  'Prototype migrated',
  'Workaround removed',
] as const

export const experimentOutcomes = [
  {
    title: 'System reuse',
    body: 'Existing components were reused instead of duplicated.',
  },
  {
    title: 'Token discipline',
    body: '0 hardcoded product colors and 0 invented semantic tokens.',
  },
  {
    title: 'Accessibility',
    body: '0 critical accessibility issues across validated workflows.',
  },
  {
    title: 'AI-assisted workflow',
    body: 'Structured design decisions made AI implementation more reliable.',
  },
] as const

export type ShowcasePrototype = {
  id: string
  name: string
  status: 'Validated'
  description: string
  metadata: string[]
  capabilities: string[]
  route: string
  cta: string
}

export const showcasePrototypes: ShowcasePrototype[] = [
  {
    id: 'access-request-review',
    name: 'Access Request Review',
    status: 'Validated',
    description:
      'An admin approval workflow for reviewing elevated system access, permissions, and risk before making a decision.',
    metadata: ['Detail workflow', 'DS v0.1 experiment'],
    capabilities: ['Forms', 'Tabs', 'Alerts', 'Dialogs', 'Permissions'],
    route: '/prototypes/access-request',
    cta: 'Open prototype',
  },
  {
    id: 'user-access-management',
    name: 'User Access Management',
    status: 'Validated',
    description:
      'A data-dense admin workflow for searching, filtering, selecting, and managing user access at scale.',
    metadata: ['Data-dense workflow', 'DS v0.2'],
    capabilities: [
      'Table',
      'Bulk selection',
      'Dropdown Menu',
      'Empty states',
      'Loading',
      'Pagination',
    ],
    route: '/prototypes/user-access-management',
    cta: 'Open prototype',
  },
]
