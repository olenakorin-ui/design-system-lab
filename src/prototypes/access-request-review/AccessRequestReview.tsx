import { useEffect, useId, useState } from 'react'
import { ArrowLeft, CircleAlert, CircleCheck } from 'lucide-react'

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

import { trackAccessRequest } from './analytics'

export type RequestStatus = 'pending' | 'approved' | 'rejected'
export type ReviewerRole = 'reviewer' | 'viewer'
export type LoadState = 'loaded' | 'error'

export type AccessRequestReviewProps = {
  requestId?: string
  initialStatus?: RequestStatus
  role?: ReviewerRole
  loadState?: LoadState
  /** Long-name stress for layout */
  longNames?: boolean
  className?: string
  onRetry?: () => void
  onBack?: () => void
}

const ACCESS_LEVELS = ['Viewer', 'Editor', 'Administrator'] as const
type AccessLevel = (typeof ACCESS_LEVELS)[number]

function statusBadge(status: RequestStatus) {
  // DS GAP: no pending/success status badges — map to existing Badge variants only.
  switch (status) {
    case 'pending':
      return <Badge variant="secondary">Pending</Badge>
    case 'approved':
      return <Badge variant="verified">Approved</Badge>
    case 'rejected':
      return <Badge variant="destructive">Rejected</Badge>
  }
}

export function AccessRequestReview({
  requestId = 'AR-1048',
  initialStatus = 'pending',
  role = 'reviewer',
  loadState = 'loaded',
  longNames = false,
  className,
  onRetry,
  onBack,
}: AccessRequestReviewProps) {
  const isViewer = role === 'viewer'
  const readOnlyDecisions = isViewer || initialStatus !== 'pending'

  const [status, setStatus] = useState<RequestStatus>(initialStatus)
  const [accessLevel, setAccessLevel] = useState<AccessLevel>('Administrator')
  const [ticket, setTicket] = useState('SEC-2841')
  const [confirmed, setConfirmed] = useState(false)
  const [feedback, setFeedback] = useState<string | null>(null)
  const [approveOpen, setApproveOpen] = useState(false)
  const [rejectOpen, setRejectOpen] = useState(false)
  const [tab, setTab] = useState('overview')

  const confirmId = useId()
  const ticketId = useId()
  const accessId = useId()

  const requestor = longNames
    ? 'Alexandra Montgomery-Cartwright III'
    : 'Alex Morgan'
  const department = longNames
    ? 'Global Product Operations & Customer Success Enablement'
    : 'Product Operations'
  const system = longNames
    ? 'Enterprise Analytics Workspace — EMEA Regional Cluster'
    : 'Analytics Workspace'

  const canDecide =
    !isViewer && status === 'pending' && confirmed && accessLevel.length > 0

  useEffect(() => {
    trackAccessRequest('access_request_viewed', {
      requestId,
      role,
      status: initialStatus,
      loadState,
    })
  }, [requestId, role, initialStatus, loadState])

  useEffect(() => {
    setStatus(initialStatus)
    setFeedback(null)
    setConfirmed(false)
    setAccessLevel('Administrator')
    setTicket('SEC-2841')
  }, [initialStatus, role, loadState])

  if (loadState === 'error') {
    return (
      <div className={cn('mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8', className)}>
        <Alert variant="destructive">
          <CircleAlert aria-hidden="true" />
          <AlertTitle>Unable to load this request.</AlertTitle>
          <AlertDescription>
            Something went wrong while loading {requestId}. Try again.
          </AlertDescription>
        </Alert>
        <div>
          <Button
            type="button"
            onClick={() => {
              trackAccessRequest('access_request_viewed', { requestId, retry: true })
              onRetry?.()
            }}
          >
            Retry
          </Button>
        </div>
      </div>
    )
  }

  const decisionsLocked = readOnlyDecisions || status !== 'pending'

  return (
    <div className={cn('mx-auto flex w-full max-w-3xl flex-col gap-6 p-4 sm:p-8', className)}>
      {/* Header */}
      <header className="flex flex-col gap-4 border-b border-border pb-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex min-w-0 flex-wrap items-center gap-3">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={onBack}
            aria-label="Back"
          >
            <ArrowLeft aria-hidden="true" />
            Back
          </Button>
          <div className="min-w-0">
            <p className="text-sm text-muted-foreground">Request ID</p>
            <h1 className="truncate text-xl font-medium text-foreground">{requestId}</h1>
          </div>
          {statusBadge(status)}
          {isViewer ? <Badge variant="outline">Viewer</Badge> : null}
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            type="button"
            variant="outline"
            disabled={decisionsLocked || !canDecide}
            onClick={() => {
              trackAccessRequest('decision_started', { requestId, decision: 'reject' })
              setRejectOpen(true)
            }}
          >
            Reject
          </Button>
          <Button
            type="button"
            disabled={decisionsLocked || !canDecide}
            onClick={() => {
              trackAccessRequest('decision_started', { requestId, decision: 'approve' })
              setApproveOpen(true)
            }}
          >
            Approve
          </Button>
        </div>
      </header>

      {/* Risk alert */}
      <Alert>
        <CircleAlert aria-hidden="true" />
        <AlertTitle>Elevated permissions requested</AlertTitle>
        <AlertDescription>
          This request includes administrative access. Review the requested permissions before
          approving.
        </AlertDescription>
      </Alert>

      {feedback ? (
        <Alert variant={status === 'rejected' ? 'destructive' : 'default'}>
          {status === 'approved' ? (
            <CircleCheck aria-hidden="true" />
          ) : (
            <CircleAlert aria-hidden="true" />
          )}
          <AlertTitle>
            {status === 'approved' ? 'Request approved' : 'Request rejected'}
          </AlertTitle>
          <AlertDescription>{feedback}</AlertDescription>
        </Alert>
      ) : null}

      <Tabs
        value={tab}
        onValueChange={(value) => {
          setTab(value)
          trackAccessRequest('access_request_tab_changed', { requestId, tab: value })
        }}
      >
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="permissions">Permissions</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-4 flex flex-col gap-6">
          <dl className="grid gap-4 sm:grid-cols-2">
            <div className="min-w-0">
              <dt className="text-sm text-muted-foreground">Requested by</dt>
              <dd className="break-words text-sm font-medium text-foreground">{requestor}</dd>
            </div>
            <div className="min-w-0">
              <dt className="text-sm text-muted-foreground">Department</dt>
              <dd className="break-words text-sm font-medium text-foreground">{department}</dd>
            </div>
            <div className="min-w-0 sm:col-span-2">
              <dt className="text-sm text-muted-foreground">System</dt>
              <dd className="break-words text-sm font-medium text-foreground">{system}</dd>
            </div>
          </dl>

          <div className="flex flex-col gap-2">
            <label htmlFor={accessId} className="text-sm font-medium text-foreground">
              Access level
            </label>
            <Select
              value={accessLevel}
              onValueChange={(value) => {
                const next = value as AccessLevel
                setAccessLevel(next)
                trackAccessRequest('access_level_changed', { requestId, accessLevel: next })
              }}
              disabled={decisionsLocked}
            >
              <SelectTrigger id={accessId} className="max-w-md">
                <SelectValue placeholder="Select access level" />
              </SelectTrigger>
              <SelectContent>
                {ACCESS_LEVELS.map((level) => (
                  <SelectItem key={level} value={level}>
                    {level}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex flex-col gap-2">
            <label htmlFor={ticketId} className="text-sm font-medium text-foreground">
              Reference ticket
            </label>
            <Input
              id={ticketId}
              name="referenceTicket"
              value={ticket}
              onChange={(e) => setTicket(e.target.value)}
              disabled={decisionsLocked}
              className="max-w-md"
            />
          </div>

          <div className="flex items-start gap-2">
            <Checkbox
              id={confirmId}
              checked={confirmed}
              disabled={decisionsLocked}
              onCheckedChange={(value) => {
                const next = value === true
                setConfirmed(next)
                trackAccessRequest('review_confirmation_checked', {
                  requestId,
                  checked: next,
                })
              }}
              className="mt-0.5"
            />
            <label htmlFor={confirmId} className="text-sm font-medium text-foreground cursor-pointer">
              I reviewed the requested permissions.
            </label>
          </div>

          <div className="flex flex-wrap gap-2 border-t border-border pt-4">
            <Button
              type="button"
              variant="outline"
              disabled={decisionsLocked || !canDecide}
              onClick={() => {
                trackAccessRequest('decision_started', { requestId, decision: 'reject' })
                setRejectOpen(true)
              }}
            >
              Reject
            </Button>
            <Button
              type="button"
              disabled={decisionsLocked || !canDecide}
              onClick={() => {
                trackAccessRequest('decision_started', { requestId, decision: 'approve' })
                setApproveOpen(true)
              }}
            >
              Approve request
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="permissions" className="mt-4 flex flex-col gap-3">
          <p className="text-sm text-muted-foreground">
            Permissions included in this request (read-only summary).
          </p>
          <ul className="flex flex-col gap-2">
            {[
              'workspace.admin',
              'datasets.write',
              'members.invite',
              'billing.view',
            ].map((perm) => (
              <li
                key={perm}
                className="flex items-center justify-between gap-3 rounded-md border border-border px-3 py-2"
              >
                <span className="font-mono text-sm text-foreground">{perm}</span>
                <Badge variant="outline">Requested</Badge>
              </li>
            ))}
          </ul>
        </TabsContent>

        <TabsContent value="activity" className="mt-4 flex flex-col gap-3">
          <ul className="flex flex-col gap-3 text-sm">
            <li className="rounded-md border border-border px-3 py-2">
              <p className="font-medium text-foreground">Request submitted</p>
              <p className="text-muted-foreground">
                {requestor} · Analytics Workspace · 2 hours ago
              </p>
            </li>
            <li className="rounded-md border border-border px-3 py-2">
              <p className="font-medium text-foreground">Routed to security review</p>
              <p className="text-muted-foreground">System · 1 hour ago</p>
            </li>
            {status !== 'pending' ? (
              <li className="rounded-md border border-border px-3 py-2">
                <p className="font-medium text-foreground">
                  Request {status === 'approved' ? 'approved' : 'rejected'}
                </p>
                <p className="text-muted-foreground">Just now</p>
              </li>
            ) : null}
          </ul>
        </TabsContent>
      </Tabs>

      {/* Approve dialog */}
      <Dialog
        open={approveOpen}
        onOpenChange={(open) => {
          setApproveOpen(open)
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Approve access request?</DialogTitle>
            <DialogDescription>
              {requestor} will receive {accessLevel} access to {system}.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  trackAccessRequest('decision_cancelled', {
                    requestId,
                    decision: 'approve',
                  })
                }}
              >
                Cancel
              </Button>
            </DialogClose>
            <Button
              type="button"
              onClick={() => {
                setStatus('approved')
                setFeedback(`${requestor} now has ${accessLevel} access to ${system}.`)
                setApproveOpen(false)
                trackAccessRequest('request_approved', {
                  requestId,
                  accessLevel,
                  ticket,
                })
              }}
            >
              Approve request
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Reject dialog */}
      <Dialog
        open={rejectOpen}
        onOpenChange={(open) => {
          setRejectOpen(open)
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Reject access request?</DialogTitle>
            <DialogDescription>The request will be marked as rejected.</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  trackAccessRequest('decision_cancelled', {
                    requestId,
                    decision: 'reject',
                  })
                }}
              >
                Cancel
              </Button>
            </DialogClose>
            <Button
              type="button"
              variant="destructive"
              onClick={() => {
                setStatus('rejected')
                setFeedback('The access request was rejected.')
                setRejectOpen(false)
                trackAccessRequest('request_rejected', { requestId, ticket })
              }}
            >
              Reject request
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
