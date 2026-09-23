import { Button } from '@/components/ui/button'
import { getPrototypeById } from '@/prototypes/registry'

import { AccessRequestReview } from '../components/AccessRequestReview'
import {
  ACCESS_REQUEST_SCENARIO_IDS,
  getAccessRequestScenario,
  type AccessRequestScenarioId,
} from '../mocks/scenarios'

export type AccessRequestPageProps = {
  scenario: AccessRequestScenarioId
  onScenarioChange: (scenario: AccessRequestScenarioId) => void
  onBack: () => void
  onRetryError: () => void
}

export function AccessRequestPage({
  scenario,
  onScenarioChange,
  onBack,
  onRetryError,
}: AccessRequestPageProps) {
  const fixture = getAccessRequestScenario(scenario)
  const meta = getPrototypeById('access-request-review')

  return (
    <div>
      <div className="border-b border-border px-4 py-3 sm:px-8">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-3">
          <p className="text-xs font-medium text-muted-foreground">
            Prototype Lab · {meta?.name ?? 'Access Request Review'} · DS{' '}
            {meta?.designSystemVersion ?? 'v0.1.0'}
          </p>
          <div className="flex flex-wrap gap-2" role="group" aria-label="Scenario">
            {ACCESS_REQUEST_SCENARIO_IDS.map((id) => {
              const active = id === scenario
              return (
                <Button
                  key={id}
                  type="button"
                  size="sm"
                  variant={active ? 'default' : 'outline'}
                  onClick={() => onScenarioChange(id)}
                >
                  {getAccessRequestScenario(id).label}
                </Button>
              )
            })}
          </div>
        </div>
      </div>

      <AccessRequestReview
        key={scenario}
        requestId={fixture.requestId}
        initialStatus={fixture.initialStatus}
        role={fixture.role}
        loadState={fixture.loadState}
        longNames={fixture.longNames}
        requestor={fixture.requestor}
        department={fixture.department}
        system={fixture.system}
        defaultAccessLevel={fixture.accessLevelDefault}
        defaultTicket={fixture.referenceTicket}
        onBack={onBack}
        onRetry={onRetryError}
      />
    </div>
  )
}
