import { useEffect, useId, useMemo, useState } from 'react'
import { ArrowLeft, CircleAlert } from 'lucide-react'

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { cn } from '@/lib/utils'

import { trackUam } from '../analytics'
import {
  ROLE_OPTIONS,
  STATUS_OPTIONS,
  type MockUser,
  type UserStatus,
} from '../mocks/users'
import type { UamScenario } from '../mocks/scenarios'

export type UserAccessManagementProps = {
  scenario: UamScenario
  onBack?: () => void
  onRetry?: () => void
  className?: string
}

function statusBadge(status: UserStatus) {
  // DS GAP: no product status tokens — map to existing Badge variants only.
  switch (status) {
    case 'Active':
      return <Badge variant="verified">Active</Badge>
    case 'Inactive':
      return <Badge variant="outline">Inactive</Badge>
    case 'Suspended':
      return <Badge variant="destructive">Suspended</Badge>
    case 'Invited':
      return <Badge variant="secondary">Invited</Badge>
  }
}

function filterUsers(
  users: MockUser[],
  query: string,
  roleFilter: string,
  statusFilter: string,
  tab: string,
): MockUser[] {
  const q = query.trim().toLowerCase()
  return users.filter((user) => {
    if (q) {
      const hay = `${user.name} ${user.email}`.toLowerCase()
      if (!hay.includes(q)) return false
    }
    if (roleFilter !== 'All roles' && user.role !== roleFilter) return false
    if (statusFilter !== 'All statuses' && user.status !== statusFilter) return false
    if (tab === 'needs-attention') {
      return user.status === 'Inactive' || user.status === 'Suspended' || user.status === 'Invited'
    }
    return true
  })
}

export function UserAccessManagement({
  scenario,
  onBack,
  onRetry,
  className,
}: UserAccessManagementProps) {
  const isViewer = scenario.role === 'viewer'
  const searchId = useId()
  const roleId = useId()
  const statusId = useId()
  const inviteEmailId = useId()

  const [query, setQuery] = useState(scenario.initialQuery)
  const [roleFilter, setRoleFilter] = useState(scenario.initialRoleFilter)
  const [statusFilter, setStatusFilter] = useState(scenario.initialStatusFilter)
  const [selectedIds, setSelectedIds] = useState<string[]>(scenario.initialSelectedIds)
  const [tab, setTab] = useState('all')
  const [inviteOpen, setInviteOpen] = useState(false)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [rowActionUser, setRowActionUser] = useState<MockUser | null>(null)
  const [inviteEmail, setInviteEmail] = useState('')
  const [feedback, setFeedback] = useState<string | null>(null)

  const sourceUsers = scenario.users ?? []

  useEffect(() => {
    setQuery(scenario.initialQuery)
    setRoleFilter(scenario.initialRoleFilter)
    setStatusFilter(scenario.initialStatusFilter)
    setSelectedIds(scenario.initialSelectedIds)
    setTab('all')
    setFeedback(null)
    setInviteEmail('')
    trackUam('uam_viewed', { scenario: scenario.id, role: scenario.role })
  }, [scenario])

  const visibleUsers = useMemo(
    () => filterUsers(sourceUsers, query, roleFilter, statusFilter, tab),
    [sourceUsers, query, roleFilter, statusFilter, tab],
  )

  const allVisibleSelected =
    visibleUsers.length > 0 && visibleUsers.every((u) => selectedIds.includes(u.id))
  const someVisibleSelected = visibleUsers.some((u) => selectedIds.includes(u.id))

  const toggleUser = (id: string, checked: boolean) => {
    setSelectedIds((prev) => {
      const next = checked ? [...new Set([...prev, id])] : prev.filter((x) => x !== id)
      trackUam('uam_selection_changed', { count: next.length })
      return next
    })
  }

  const toggleAllVisible = (checked: boolean) => {
    setSelectedIds((prev) => {
      const visibleIds = visibleUsers.map((u) => u.id)
      const next = checked
        ? [...new Set([...prev, ...visibleIds])]
        : prev.filter((id) => !visibleIds.includes(id))
      trackUam('uam_selection_changed', { count: next.length, selectAll: checked })
      return next
    })
  }

  if (scenario.loadState === 'error') {
    return (
      <div className={cn('mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8', className)}>
        <Alert variant="destructive">
          <CircleAlert aria-hidden="true" />
          <AlertTitle>Unable to load users.</AlertTitle>
          <AlertDescription>Something went wrong while loading the directory.</AlertDescription>
        </Alert>
        <div>
          <Button type="button" onClick={() => onRetry?.()}>
            Retry
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className={cn('mx-auto flex w-full max-w-5xl flex-col gap-6 p-4 sm:p-8', className)}>
      <header className="flex flex-col gap-4 border-b border-border pb-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 flex flex-col gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="w-fit"
            onClick={onBack}
            aria-label="Back to hub"
          >
            <ArrowLeft aria-hidden="true" />
            Back
          </Button>
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-xl font-medium text-foreground">User Access Management</h1>
            {isViewer ? <Badge variant="outline">Viewer</Badge> : null}
          </div>
          <p className="max-w-2xl text-sm text-muted-foreground">
            Review users, filter by role and status, and take action on selected accounts.
          </p>
        </div>
        <Button
          type="button"
          disabled={isViewer || scenario.loadState === 'loading'}
          onClick={() => {
            trackUam('uam_invite_started')
            setInviteOpen(true)
          }}
        >
          Invite user
        </Button>
      </header>

      {feedback ? (
        <Alert>
          <AlertTitle>Action completed</AlertTitle>
          <AlertDescription>{feedback}</AlertDescription>
        </Alert>
      ) : null}

      {scenario.loadState === 'loading' ? (
        <Alert>
          <CircleAlert aria-hidden="true" />
          <AlertTitle>Loading users…</AlertTitle>
          <AlertDescription>
            {/* DS GAP: no Skeleton primitive — Alert used as loading feedback. */}
            Fetching the directory. Controls are temporarily unavailable.
          </AlertDescription>
        </Alert>
      ) : null}

      <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-end">
        <div className="flex min-w-0 flex-1 flex-col gap-2">
          <label htmlFor={searchId} className="text-sm font-medium text-foreground">
            Search users
          </label>
          <Input
            id={searchId}
            type="search"
            placeholder="Search by name or email"
            value={query}
            disabled={scenario.loadState === 'loading'}
            onChange={(e) => {
              const next = e.target.value
              setQuery(next)
              trackUam('uam_search_changed', { query: next })
            }}
          />
        </div>
        <div className="flex w-full flex-col gap-2 sm:w-44">
          <label htmlFor={roleId} className="text-sm font-medium text-foreground">
            Role
          </label>
          <Select
            value={roleFilter}
            disabled={scenario.loadState === 'loading'}
            onValueChange={(value) => {
              setRoleFilter(value)
              trackUam('uam_filter_changed', { filter: 'role', value })
            }}
          >
            <SelectTrigger id={roleId}>
              <SelectValue placeholder="Role" />
            </SelectTrigger>
            <SelectContent>
              {ROLE_OPTIONS.map((role) => (
                <SelectItem key={role} value={role}>
                  {role}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex w-full flex-col gap-2 sm:w-44">
          <label htmlFor={statusId} className="text-sm font-medium text-foreground">
            Status
          </label>
          <Select
            value={statusFilter}
            disabled={scenario.loadState === 'loading'}
            onValueChange={(value) => {
              setStatusFilter(value)
              trackUam('uam_filter_changed', { filter: 'status', value })
            }}
          >
            <SelectTrigger id={statusId}>
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              {STATUS_OPTIONS.map((status) => (
                <SelectItem key={status} value={status}>
                  {status}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {!isViewer && selectedIds.length > 0 && scenario.loadState === 'loaded' ? (
        <div className="flex flex-wrap items-center gap-3 rounded-md border border-border px-3 py-2">
          <p className="text-sm text-foreground">
            {selectedIds.length} selected
          </p>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => {
              trackUam('uam_bulk_started', { count: selectedIds.length })
              setBulkOpen(true)
            }}
          >
            Deactivate selected
          </Button>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => {
              setSelectedIds([])
              trackUam('uam_selection_changed', { count: 0 })
            }}
          >
            Clear selection
          </Button>
        </div>
      ) : null}

      <Tabs
        value={tab}
        onValueChange={(value) => {
          setTab(value)
          trackUam('uam_tab_changed', { tab: value })
        }}
      >
        <TabsList>
          <TabsTrigger value="all" disabled={scenario.loadState === 'loading'}>
            All users
          </TabsTrigger>
          <TabsTrigger value="needs-attention" disabled={scenario.loadState === 'loading'}>
            Needs attention
          </TabsTrigger>
        </TabsList>

        <TabsContent value={tab} className="mt-4">
          {scenario.loadState === 'loading' ? (
            <p className="text-sm text-muted-foreground">User list will appear when loading finishes.</p>
          ) : visibleUsers.length === 0 ? (
            <Alert>
              <CircleAlert aria-hidden="true" />
              <AlertTitle>No users found</AlertTitle>
              <AlertDescription>
                {/* DS GAP: no Empty State component — Alert used for empty results. */}
                Try adjusting search or filters.
              </AlertDescription>
            </Alert>
          ) : (
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2 border-b border-border pb-2">
                <Checkbox
                  checked={
                    allVisibleSelected ? true : someVisibleSelected ? 'indeterminate' : false
                  }
                  disabled={isViewer}
                  onCheckedChange={(value) => toggleAllVisible(value === true)}
                  aria-label="Select all visible users"
                />
                <span className="text-sm text-muted-foreground">
                  {visibleUsers.length} user{visibleUsers.length === 1 ? '' : 's'}
                </span>
              </div>

              <ul className="flex flex-col gap-2" aria-label="Users">
                {visibleUsers.map((user) => {
                  const selected = selectedIds.includes(user.id)
                  return (
                    <li
                      key={user.id}
                      className="rounded-md border border-border px-3 py-3"
                    >
                      <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                        <div className="flex min-w-0 flex-1 gap-3">
                          <Checkbox
                            checked={selected}
                            disabled={isViewer}
                            onCheckedChange={(value) => toggleUser(user.id, value === true)}
                            aria-label={`Select ${user.name}`}
                            className="mt-1"
                          />
                          <div className="min-w-0 flex flex-1 flex-col gap-2">
                            <div className="flex flex-wrap items-center gap-2">
                              <p className="break-words text-sm font-medium text-foreground">
                                {user.name}
                              </p>
                              {statusBadge(user.status)}
                            </div>
                            <p className="break-all text-sm text-muted-foreground">{user.email}</p>
                            <dl className="grid gap-2 text-sm sm:grid-cols-3">
                              <div>
                                <dt className="text-muted-foreground">Role</dt>
                                <dd className="text-foreground">{user.role}</dd>
                              </div>
                              <div>
                                <dt className="text-muted-foreground">Access level</dt>
                                <dd className="text-foreground">{user.accessLevel}</dd>
                              </div>
                              <div>
                                <dt className="text-muted-foreground">Last active</dt>
                                <dd className="text-foreground">{user.lastActive}</dd>
                              </div>
                            </dl>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 lg:justify-end">
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            disabled={isViewer}
                            onClick={() => {
                              trackUam('uam_row_action', { action: 'deactivate', userId: user.id })
                              setRowActionUser(user)
                            }}
                          >
                            Deactivate
                          </Button>
                        </div>
                      </div>
                    </li>
                  )
                })}
              </ul>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {/* Invite dialog */}
      <Dialog open={inviteOpen} onOpenChange={setInviteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invite user</DialogTitle>
            <DialogDescription>
              Send an invitation email. No users are persisted in this prototype.
            </DialogDescription>
          </DialogHeader>
          <div className="flex flex-col gap-2 py-2">
            <label htmlFor={inviteEmailId} className="text-sm font-medium text-foreground">
              Email
            </label>
            <Input
              id={inviteEmailId}
              type="email"
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              placeholder="name@example.com"
            />
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button
                type="button"
                variant="outline"
                onClick={() => trackUam('uam_invite_cancelled')}
              >
                Cancel
              </Button>
            </DialogClose>
            <Button
              type="button"
              disabled={!inviteEmail.trim()}
              onClick={() => {
                trackUam('uam_invite_submitted', { email: inviteEmail.trim() })
                setFeedback(`Invitation queued for ${inviteEmail.trim()}.`)
                setInviteOpen(false)
                setInviteEmail('')
              }}
            >
              Send invite
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Bulk deactivate */}
      <Dialog open={bulkOpen} onOpenChange={setBulkOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Deactivate selected users?</DialogTitle>
            <DialogDescription>
              {selectedIds.length} account{selectedIds.length === 1 ? '' : 's'} will be marked
              inactive in this prototype session.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button
                type="button"
                variant="outline"
                onClick={() => trackUam('uam_bulk_cancelled')}
              >
                Cancel
              </Button>
            </DialogClose>
            <Button
              type="button"
              variant="destructive"
              onClick={() => {
                trackUam('uam_bulk_confirmed', { count: selectedIds.length })
                setFeedback(`Deactivated ${selectedIds.length} user(s).`)
                setSelectedIds([])
                setBulkOpen(false)
              }}
            >
              Deactivate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Row deactivate */}
      <Dialog
        open={rowActionUser !== null}
        onOpenChange={(open) => {
          if (!open) setRowActionUser(null)
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Deactivate user?</DialogTitle>
            <DialogDescription>
              {rowActionUser
                ? `${rowActionUser.name} (${rowActionUser.email}) will be marked inactive in this prototype session.`
                : null}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button type="button" variant="outline">
                Cancel
              </Button>
            </DialogClose>
            <Button
              type="button"
              variant="destructive"
              onClick={() => {
                if (rowActionUser) {
                  trackUam('uam_row_action', {
                    action: 'deactivate_confirmed',
                    userId: rowActionUser.id,
                  })
                  setFeedback(`${rowActionUser.name} was deactivated.`)
                }
                setRowActionUser(null)
              }}
            >
              Deactivate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
