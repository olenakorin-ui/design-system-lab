import { Button } from '@/components/ui/button'
import { getPrototypeById } from '@/prototypes/registry'

import { UserAccessManagement } from '../components/UserAccessManagement'
import {
  getUamScenario,
  UAM_SCENARIO_IDS,
  type UamScenarioId,
} from '../mocks/scenarios'

export type UserAccessManagementPageProps = {
  scenario: UamScenarioId
  onScenarioChange: (scenario: UamScenarioId) => void
  onBack: () => void
  onRetryError: () => void
}

export function UserAccessManagementPage({
  scenario,
  onScenarioChange,
  onBack,
  onRetryError,
}: UserAccessManagementPageProps) {
  const fixture = getUamScenario(scenario)
  const meta = getPrototypeById('user-access-management')

  return (
    <div>
      <div className="border-b border-border px-4 py-3 sm:px-8">
        <div className="mx-auto flex w-full max-w-5xl flex-col gap-3">
          <p className="text-xs font-medium text-muted-foreground">
            Prototype Lab · {meta?.name ?? 'User Access Management'} · DS{' '}
            {meta?.designSystemVersion ?? 'v0.1.0'}
          </p>
          <div className="flex flex-wrap gap-2" role="group" aria-label="Scenario">
            {UAM_SCENARIO_IDS.map((id) => {
              const active = id === scenario
              return (
                <Button
                  key={id}
                  type="button"
                  size="sm"
                  variant={active ? 'default' : 'outline'}
                  onClick={() => onScenarioChange(id)}
                >
                  {getUamScenario(id).label}
                </Button>
              )
            })}
          </div>
        </div>
      </div>

      <UserAccessManagement
        key={scenario}
        scenario={fixture}
        onBack={onBack}
        onRetry={onRetryError}
      />
    </div>
  )
}
