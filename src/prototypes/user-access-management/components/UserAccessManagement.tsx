import { useEffect, useId, useMemo, useRef, useState } from 'react'
import { ArrowLeft, CircleAlert, Inbox, MoreHorizontal, Search } from 'lucide-react'

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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  EmptyState,
  EmptyStateActions,
  EmptyStateDescription,
  EmptyStateHeader,
  EmptyStateIcon,
  EmptyStateTitle,
} from '@/components/ui/empty-state'
import { Input } from '@/components/ui/input'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { cn } from '@/lib/utils'

import { trackUam } from '../analytics'
import {
  ROLE_OPTIONS,
  STATUS_OPTIONS,
  type MockUser,
  type UserStatus,
} from '../mocks/users'
import { UAM_PAGE_SIZE, type UamScenario } from '../mocks/scenarios'

export type UserAccessManagementProps = {
  scenario: UamScenario
  onBack?: () => void
  onRetry?: () => void
  className?: string
}

/**
 * Selection model (documented):
 * - `selectedIds` persist across pages.
 * - Header “Select all” toggles only rows on the **current page**.
 * - Bulk bar counts all selected ids across pages.
 */
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

function pageWindow(current: number, total: number): (number | 'ellipsis')[] {
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  const pages: (number | 'ellipsis')[] = [1]
  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  if (start > 2) pages.push('ellipsis')
  for (let p = start; p <= end; p += 1) pages.push(p)
  if (end < total - 1) pages.push('ellipsis')
  pages.push(total)
  return pages
}

function DirectorySkeleton() {
  return (
    <div
      className="flex flex-col gap-3"
      aria-busy="true"
      aria-live="polite"
      aria-label="Loading users"
    >
      <div className="flex items-center gap-3 border-b border-border pb-3">
        <Skeleton className="size-4 shrink-0 rounded-sm" />
        <Skeleton className="h-4 w-16" />
        <Skeleton className="h-4 w-28" />
        <Skeleton className="h-4 w-14" />
        <Skeleton className="h-4 w-16" />
        <Skeleton className="h-4 w-16" />
        <Skeleton className="h-4 w-20" />
      </div>
      {Array.from({ length: UAM_PAGE_SIZE }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 py-1">
          <Skeleton className="size-4 shrink-0 rounded-sm" />
          <Skeleton className="h-4 w-28" />
          <Skeleton className="h-4 min-w-0 flex-1" />
          <Skeleton className="h-4 w-14" />
          <Skeleton className="h-4 w-16" />
          <Skeleton className="h-5 w-16 rounded-full" />
          <Skeleton className="h-4 w-20" />
          <Skeleton className="size-8 shrink-0 rounded-md" />
        </div>
      ))}
    </div>
  )
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
  const [page, setPage] = useState(() => Math.max(1, scenario.initialPage))
  const [inviteOpen, setInviteOpen] = useState(false)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [rowActionUser, setRowActionUser] = useState<MockUser | null>(null)
  const [inviteEmail, setInviteEmail] = useState('')
  const [feedback, setFeedback] = useState<string | null>(null)
  const skipFilterPageReset = useRef(true)

  const sourceUsers = scenario.users ?? []
  const hasDirectoryData = sourceUsers.length > 0
  const hasActiveFilters =
    query.trim() !== '' ||
    roleFilter !== 'All roles' ||
    statusFilter !== 'All statuses' ||
    tab !== 'all'

  useEffect(() => {
    setQuery(scenario.initialQuery)
    setRoleFilter(scenario.initialRoleFilter)
    setStatusFilter(scenario.initialStatusFilter)
    setSelectedIds(scenario.initialSelectedIds)
    setTab('all')
    setPage(Math.max(1, scenario.initialPage))
    setFeedback(null)
    setInviteEmail('')
    skipFilterPageReset.current = true
    trackUam('uam_viewed', { scenario: scenario.id, role: scenario.role })
  }, [scenario])

  const visibleUsers = useMemo(
    () => filterUsers(sourceUsers, query, roleFilter, statusFilter, tab),
    [sourceUsers, query, roleFilter, statusFilter, tab],
  )

  const totalPages = Math.max(1, Math.ceil(visibleUsers.length / UAM_PAGE_SIZE))

  useEffect(() => {
    setPage((prev) => Math.min(Math.max(1, prev), totalPages))
  }, [totalPages])

  useEffect(() => {
    if (skipFilterPageReset.current) {
      skipFilterPageReset.current = false
      return
    }
    setPage(1)
  }, [query, roleFilter, statusFilter, tab])

  const goToPage = (next: number) => {
    const clamped = Math.min(Math.max(1, next), totalPages)
    setPage(clamped)
    trackUam('user_directory_page_changed', { page: clamped, totalPages })
  }

  const pageUsers = useMemo(() => {
    const start = (page - 1) * UAM_PAGE_SIZE
    return visibleUsers.slice(start, start + UAM_PAGE_SIZE)
  }, [visibleUsers, page])

  const allPageSelected =
    pageUsers.length > 0 && pageUsers.every((u) => selectedIds.includes(u.id))
  const somePageSelected = pageUsers.some((u) => selectedIds.includes(u.id))

  const toggleUser = (id: string, checked: boolean) => {
    setSelectedIds((prev) => {
      const next = checked ? [...new Set([...prev, id])] : prev.filter((x) => x !== id)
      trackUam('uam_selection_changed', { count: next.length })
      return next
    })
  }

  const toggleAllPage = (checked: boolean) => {
    setSelectedIds((prev) => {
      const pageIds = pageUsers.map((u) => u.id)
      const next = checked
        ? [...new Set([...prev, ...pageIds])]
        : prev.filter((id) => !pageIds.includes(id))
      trackUam('uam_selection_changed', {
        count: next.length,
        selectAll: checked,
        scope: 'page',
      })
      return next
    })
  }

  const clearFilters = () => {
    skipFilterPageReset.current = true
    setQuery('')
    setRoleFilter('All roles')
    setStatusFilter('All statuses')
    setTab('all')
    setPage(1)
    trackUam('user_directory_filters_cleared', {})
    trackUam('uam_filter_changed', { filter: 'clear_all', value: '' })
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
            disabled={scenario.loadState === 'loading' || !hasDirectoryData}
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
            disabled={scenario.loadState === 'loading' || !hasDirectoryData}
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
            disabled={scenario.loadState === 'loading' || !hasDirectoryData}
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
          <p className="text-sm text-foreground">{selectedIds.length} selected</p>
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
          <TabsTrigger
            value="all"
            disabled={scenario.loadState === 'loading' || !hasDirectoryData}
          >
            All users
          </TabsTrigger>
          <TabsTrigger
            value="needs-attention"
            disabled={scenario.loadState === 'loading' || !hasDirectoryData}
          >
            Needs attention
          </TabsTrigger>
        </TabsList>

        <TabsContent value={tab} className="mt-4 flex flex-col gap-4">
          {scenario.loadState === 'loading' ? (
            <DirectorySkeleton />
          ) : !hasDirectoryData ? (
            <EmptyState className="mx-auto">
              <EmptyStateIcon>
                <Inbox aria-hidden="true" />
              </EmptyStateIcon>
              <EmptyStateHeader>
                <EmptyStateTitle>No users yet</EmptyStateTitle>
                <EmptyStateDescription>
                  Invite your first user to start managing access.
                </EmptyStateDescription>
              </EmptyStateHeader>
              {!isViewer ? (
                <EmptyStateActions>
                  <Button
                    type="button"
                    onClick={() => {
                      trackUam('user_directory_empty_action_clicked', {
                        action: 'invite_user',
                      })
                      trackUam('uam_invite_started')
                      setInviteOpen(true)
                    }}
                  >
                    Invite user
                  </Button>
                </EmptyStateActions>
              ) : null}
            </EmptyState>
          ) : visibleUsers.length === 0 ? (
            <EmptyState className="mx-auto">
              <EmptyStateIcon>
                <Search aria-hidden="true" />
              </EmptyStateIcon>
              <EmptyStateHeader>
                <EmptyStateTitle>No users found</EmptyStateTitle>
                <EmptyStateDescription>
                  Try changing your search or filters.
                </EmptyStateDescription>
              </EmptyStateHeader>
              {hasActiveFilters ? (
                <EmptyStateActions>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => {
                      trackUam('user_directory_empty_action_clicked', {
                        action: 'clear_filters',
                      })
                      clearFilters()
                    }}
                  >
                    Clear filters
                  </Button>
                </EmptyStateActions>
              ) : null}
            </EmptyState>
          ) : (
            <>
              <Table>
                <TableCaption className="sr-only">
                  User directory. Narrow viewports scroll horizontally (D009). Page {page} of{' '}
                  {totalPages}.
                </TableCaption>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-10">
                      <Checkbox
                        checked={
                          allPageSelected ? true : somePageSelected ? 'indeterminate' : false
                        }
                        disabled={isViewer}
                        onCheckedChange={(value) => toggleAllPage(value === true)}
                        aria-label="Select all users on this page"
                      />
                    </TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Access</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Last active</TableHead>
                    <TableHead className="w-12">
                      <span className="sr-only">Actions</span>
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {pageUsers.map((user) => {
                    const selected = selectedIds.includes(user.id)
                    return (
                      <TableRow
                        key={user.id}
                        data-state={selected ? 'selected' : undefined}
                      >
                        <TableCell>
                          <Checkbox
                            checked={selected}
                            disabled={isViewer}
                            onCheckedChange={(value) =>
                              toggleUser(user.id, value === true)
                            }
                            aria-label={`Select ${user.name}`}
                          />
                        </TableCell>
                        <TableCell className="font-medium whitespace-nowrap">
                          {user.name}
                        </TableCell>
                        <TableCell className="max-w-[16rem] truncate" title={user.email}>
                          {user.email}
                        </TableCell>
                        <TableCell className="whitespace-nowrap">{user.role}</TableCell>
                        <TableCell className="whitespace-nowrap">
                          {user.accessLevel}
                        </TableCell>
                        <TableCell>{statusBadge(user.status)}</TableCell>
                        <TableCell className="whitespace-nowrap text-muted-foreground">
                          {user.lastActive}
                        </TableCell>
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                type="button"
                                variant="ghost"
                                size="icon"
                                disabled={isViewer}
                                aria-label={`Actions for ${user.name}`}
                              >
                                <MoreHorizontal aria-hidden="true" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem
                                onSelect={() => {
                                  trackUam('uam_row_action', {
                                    action: 'view',
                                    userId: user.id,
                                  })
                                  setFeedback(`Viewing ${user.name} (prototype).`)
                                }}
                              >
                                View
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onSelect={() => {
                                  trackUam('uam_row_action', {
                                    action: 'edit_access',
                                    userId: user.id,
                                  })
                                  setFeedback(`Edit access for ${user.name} (prototype).`)
                                }}
                              >
                                Edit access
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem
                                variant="destructive"
                                onSelect={() => {
                                  trackUam('uam_row_action', {
                                    action: 'deactivate',
                                    userId: user.id,
                                  })
                                  setRowActionUser(user)
                                }}
                              >
                                Deactivate
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>

              {visibleUsers.length > UAM_PAGE_SIZE ? (
                <Pagination>
                  <PaginationContent>
                    <PaginationItem>
                      <PaginationPrevious
                        aria-label="Go to previous page"
                        disabled={page <= 1}
                        onClick={() => goToPage(page - 1)}
                      />
                    </PaginationItem>
                    {pageWindow(page, totalPages).map((item, index) =>
                      item === 'ellipsis' ? (
                        <PaginationItem key={`e-${index}`}>
                          <PaginationEllipsis />
                        </PaginationItem>
                      ) : (
                        <PaginationItem key={item}>
                          <PaginationLink
                            isActive={page === item}
                            aria-label={`Page ${item}`}
                            onClick={() => goToPage(item)}
                          >
                            {item}
                          </PaginationLink>
                        </PaginationItem>
                      ),
                    )}
                    <PaginationItem>
                      <PaginationNext
                        aria-label="Go to next page"
                        disabled={page >= totalPages}
                        onClick={() => goToPage(page + 1)}
                      />
                    </PaginationItem>
                  </PaginationContent>
                </Pagination>
              ) : null}
            </>
          )}
        </TabsContent>
      </Tabs>

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
