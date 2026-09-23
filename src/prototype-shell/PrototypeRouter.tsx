import { useCallback, useEffect, useState } from 'react'

import { Button } from '@/components/ui/button'
import { AccessRequestPage } from '@/prototypes/access-request-review/pages/AccessRequestPage'
import {
  parseAccessRequestScenario,
  type AccessRequestScenarioId,
} from '@/prototypes/access-request-review/mocks/scenarios'
import { getPrototypeByRoute } from '@/prototypes/registry'

import { PrototypeIndex, usePersistedTheme } from './PrototypeIndex'

type LocationState = {
  pathname: string
  search: string
}

function readLocation(): LocationState {
  return {
    pathname: window.location.pathname,
    search: window.location.search,
  }
}

function navigate(to: string, { replace = false }: { replace?: boolean } = {}) {
  if (replace) {
    window.history.replaceState({}, '', to)
  } else {
    window.history.pushState({}, '', to)
  }
  window.dispatchEvent(new PopStateEvent('popstate'))
}

function buildAccessRequestPath(scenario: AccessRequestScenarioId) {
  const params = new URLSearchParams()
  if (scenario !== 'pending') {
    params.set('scenario', scenario)
  }
  const qs = params.toString()
  return qs ? `/prototypes/access-request?${qs}` : '/prototypes/access-request'
}

export function PrototypeRouter() {
  const [location, setLocation] = useState<LocationState>(readLocation)
  const [theme, setTheme] = usePersistedTheme('light')

  useEffect(() => {
    const onPop = () => setLocation(readLocation())
    window.addEventListener('popstate', onPop)
    return () => window.removeEventListener('popstate', onPop)
  }, [])

  const go = useCallback((to: string, opts?: { replace?: boolean }) => {
    navigate(to, opts)
    setLocation(readLocation())
  }, [])

  const params = new URLSearchParams(location.search)
  const scenario = parseAccessRequestScenario(params.get('scenario'))

  const isAccessRequest =
    location.pathname === '/prototypes/access-request' ||
    Boolean(getPrototypeByRoute(location.pathname)?.id === 'access-request-review')

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="flex items-center justify-end gap-2 border-b border-border px-4 py-2 sm:px-8">
        <span className="mr-auto text-xs text-muted-foreground">Prototype Lab</span>
        <Button
          type="button"
          size="sm"
          variant={theme === 'light' ? 'secondary' : 'outline'}
          onClick={() => setTheme('light')}
        >
          Light
        </Button>
        <Button
          type="button"
          size="sm"
          variant={theme === 'dark' ? 'secondary' : 'outline'}
          onClick={() => setTheme('dark')}
        >
          Dark
        </Button>
      </div>

      {location.pathname === '/' || location.pathname === '' ? (
        <PrototypeIndex onOpen={(route) => go(route)} />
      ) : isAccessRequest ? (
        <AccessRequestPage
          scenario={scenario}
          onScenarioChange={(next) => go(buildAccessRequestPath(next))}
          onBack={() => go('/')}
          onRetryError={() => go(buildAccessRequestPath('pending'), { replace: true })}
        />
      ) : (
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-4 p-8">
          <p className="text-sm text-foreground">Prototype not found.</p>
          <Button type="button" variant="outline" onClick={() => go('/')}>
            Back to hub
          </Button>
        </div>
      )}
    </div>
  )
}
