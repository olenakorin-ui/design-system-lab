export type UserRole = 'Admin' | 'Editor' | 'Viewer' | 'Security'
export type AccessLevel = 'Full' | 'Standard' | 'Limited' | 'Read-only'
export type UserStatus = 'Active' | 'Inactive' | 'Suspended' | 'Invited'

export type MockUser = {
  id: string
  name: string
  email: string
  role: UserRole
  accessLevel: AccessLevel
  status: UserStatus
  lastActive: string
}

export const MOCK_USERS: MockUser[] = [
  {
    id: 'u-01',
    name: 'Alex Morgan',
    email: 'alex.morgan@example.com',
    role: 'Admin',
    accessLevel: 'Full',
    status: 'Active',
    lastActive: '2 hours ago',
  },
  {
    id: 'u-02',
    name: 'Jordan Lee',
    email: 'jordan.lee@example.com',
    role: 'Editor',
    accessLevel: 'Standard',
    status: 'Active',
    lastActive: 'Yesterday',
  },
  {
    id: 'u-03',
    name: 'Sam Rivera',
    email: 'sam.rivera@example.com',
    role: 'Viewer',
    accessLevel: 'Read-only',
    status: 'Inactive',
    lastActive: '28 days ago',
  },
  {
    id: 'u-04',
    name: 'Casey Nguyen',
    email: 'casey.nguyen@example.com',
    role: 'Security',
    accessLevel: 'Full',
    status: 'Active',
    lastActive: 'Just now',
  },
  {
    id: 'u-05',
    name: 'Taylor Brooks',
    email: 'taylor.brooks@example.com',
    role: 'Editor',
    accessLevel: 'Standard',
    status: 'Suspended',
    lastActive: '5 days ago',
  },
  {
    id: 'u-06',
    name: 'Riley Quinn',
    email: 'riley.quinn@example.com',
    role: 'Viewer',
    accessLevel: 'Limited',
    status: 'Invited',
    lastActive: 'Never',
  },
  {
    id: 'u-07',
    name: 'Morgan Patel',
    email: 'morgan.patel@example.com',
    role: 'Editor',
    accessLevel: 'Standard',
    status: 'Active',
    lastActive: '3 hours ago',
  },
  {
    id: 'u-08',
    name: 'Avery Chen',
    email: 'avery.chen@example.com',
    role: 'Admin',
    accessLevel: 'Full',
    status: 'Active',
    lastActive: '1 hour ago',
  },
  {
    id: 'u-09',
    name: 'Jamie Okonkwo',
    email: 'jamie.okonkwo@example.com',
    role: 'Viewer',
    accessLevel: 'Read-only',
    status: 'Active',
    lastActive: '4 days ago',
  },
  {
    id: 'u-10',
    name: 'Cameron Diaz-Whitfield',
    email: 'cameron.diaz-whitfield@example.com',
    role: 'Editor',
    accessLevel: 'Limited',
    status: 'Inactive',
    lastActive: '60 days ago',
  },
  {
    id: 'u-11',
    name: 'Alexandra Montgomery-Cartwright III',
    email:
      'alexandra.montgomery-cartwright.operations.emea@long-enterprise-domain.example.com',
    role: 'Admin',
    accessLevel: 'Full',
    status: 'Active',
    lastActive: '12 minutes ago',
  },
  {
    id: 'u-12',
    name: 'Priya Shah',
    email: 'priya.shah@example.com',
    role: 'Security',
    accessLevel: 'Standard',
    status: 'Active',
    lastActive: '6 hours ago',
  },
]

export const ROLE_OPTIONS = ['All roles', 'Admin', 'Editor', 'Viewer', 'Security'] as const
export const STATUS_OPTIONS = [
  'All statuses',
  'Active',
  'Inactive',
  'Suspended',
  'Invited',
] as const
