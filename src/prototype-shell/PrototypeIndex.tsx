import { useEffect, useState } from 'react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { prototypes, type PrototypeStatus } from '@/prototypes/registry'

function statusLabel(status: PrototypeStatus) {
  switch (status) {
    case 'validated':
      return 'Validated'
    case 'in-progress':
      return 'In progress'
    case 'archived':
      return 'Archived'
    default:
      return 'Draft'
  }
}

function statusVariant(
  status: PrototypeStatus,
): 'verified' | 'secondary' | 'outline' | 'destructive' {
  switch (status) {
    case 'validated':
      return 'verified'
    case 'in-progress':
      return 'secondary'
    case 'archived':
      return 'outline'
    default:
      return 'outline'
  }
}

export type PrototypeIndexProps = {
  onOpen: (route: string) => void
}

export function PrototypeIndex({ onOpen }: PrototypeIndexProps) {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 p-4 sm:p-8">
      <header className="flex flex-col gap-2 border-b border-border pb-6">
        <p className="text-sm text-muted-foreground">Prototype Lab</p>
        <h1 className="text-2xl font-medium text-foreground">Available prototypes</h1>
        <p className="max-w-xl text-sm text-muted-foreground">
          Product flows validated against the Design System. Open a prototype to exercise
          scenarios end-to-end.
        </p>
      </header>

      <ul className="flex flex-col gap-4">
        {prototypes.map((prototype) => (
          <li
            key={prototype.id}
            className="flex flex-col gap-4 rounded-lg border border-border p-4 sm:flex-row sm:items-center sm:justify-between"
          >
            <div className="min-w-0 flex flex-col gap-2">
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-medium text-foreground">{prototype.name}</h2>
                <Badge variant={statusVariant(prototype.status)}>
                  {statusLabel(prototype.status)}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">{prototype.description}</p>
              <p className="text-xs text-muted-foreground">
                Design System: {prototype.designSystemVersion}
              </p>
            </div>
            <Button type="button" onClick={() => onOpen(prototype.route)}>
              Open prototype
            </Button>
          </li>
        ))}
      </ul>
    </div>
  )
}

/** Ensures light/dark class is applied for hub mount (theme controlled by shell). */
export function useDocumentThemeClass(theme: 'light' | 'dark') {
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])
}

export function usePersistedTheme(defaultTheme: 'light' | 'dark' = 'light') {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    try {
      const stored = localStorage.getItem('prototype-lab:theme')
      if (stored === 'light' || stored === 'dark') return stored
    } catch {
      /* ignore */
    }
    return defaultTheme
  })

  useDocumentThemeClass(theme)

  const setAndPersist = (next: 'light' | 'dark') => {
    setTheme(next)
    try {
      localStorage.setItem('prototype-lab:theme', next)
    } catch {
      /* ignore */
    }
  }

  return [theme, setAndPersist] as const
}
