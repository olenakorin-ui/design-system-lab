export type PrototypeStatus = 'draft' | 'in-progress' | 'validated' | 'archived'

export type PrototypeMeta = {
  id: string
  name: string
  description: string
  status: PrototypeStatus
  route: string
  designSystemVersion: string
}

export const prototypes: PrototypeMeta[] = [
  {
    id: 'access-request-review',
    name: 'Access Request Review',
    description: 'Admin workflow for reviewing elevated system access.',
    status: 'validated',
    route: '/prototypes/access-request',
    designSystemVersion: 'v0.1.0',
  },
  {
    id: 'user-access-management',
    name: 'User Access Management',
    description: 'Admin directory for reviewing, filtering, and acting on user accounts.',
    status: 'validated',
    route: '/prototypes/user-access-management',
    designSystemVersion: 'v0.1.0',
  },
]

export function getPrototypeById(id: string): PrototypeMeta | undefined {
  return prototypes.find((p) => p.id === id)
}

export function getPrototypeByRoute(pathname: string): PrototypeMeta | undefined {
  return prototypes.find((p) => p.route === pathname)
}
