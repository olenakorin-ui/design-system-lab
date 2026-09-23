import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  AccessRequestReview,
  type LoadState,
  type RequestStatus,
  type ReviewerRole,
} from '@/prototypes/access-request-review/AccessRequestReview'

export default function App() {
  const [status, setStatus] = useState<RequestStatus>('pending')
  const [role, setRole] = useState<ReviewerRole>('reviewer')
  const [loadState, setLoadState] = useState<LoadState>('loaded')
  const [longNames, setLongNames] = useState(false)

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="border-b border-border px-4 py-3 sm:px-8">
        <p className="mb-2 text-xs font-medium text-muted-foreground">
          Experiment harness — Access Request Review (DS v0.1.0)
        </p>
        <div className="flex flex-wrap gap-2">
          <Button
            size="sm"
            variant={status === 'pending' ? 'default' : 'outline'}
            onClick={() => {
              setStatus('pending')
              setLoadState('loaded')
            }}
          >
            Pending
          </Button>
          <Button
            size="sm"
            variant={status === 'approved' ? 'default' : 'outline'}
            onClick={() => {
              setStatus('approved')
              setLoadState('loaded')
            }}
          >
            Approved
          </Button>
          <Button
            size="sm"
            variant={status === 'rejected' ? 'default' : 'outline'}
            onClick={() => {
              setStatus('rejected')
              setLoadState('loaded')
            }}
          >
            Rejected
          </Button>
          <Button
            size="sm"
            variant={role === 'reviewer' ? 'secondary' : 'outline'}
            onClick={() => setRole('reviewer')}
          >
            Reviewer
          </Button>
          <Button
            size="sm"
            variant={role === 'viewer' ? 'secondary' : 'outline'}
            onClick={() => setRole('viewer')}
          >
            Viewer
          </Button>
          <Button
            size="sm"
            variant={loadState === 'error' ? 'destructive' : 'outline'}
            onClick={() => setLoadState(loadState === 'error' ? 'loaded' : 'error')}
          >
            Toggle error
          </Button>
          <Button
            size="sm"
            variant={longNames ? 'secondary' : 'outline'}
            onClick={() => setLongNames((v) => !v)}
          >
            Long names
          </Button>
        </div>
      </div>
      <AccessRequestReview
        key={`${status}-${role}-${loadState}-${longNames}`}
        initialStatus={status}
        role={role}
        loadState={loadState}
        longNames={longNames}
        onRetry={() => setLoadState('loaded')}
      />
    </div>
  )
}
