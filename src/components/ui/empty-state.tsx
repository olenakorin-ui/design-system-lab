import * as React from 'react'

import { cn } from '@/lib/utils'

function EmptyState({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="empty-state"
      className={cn(
        'flex w-full max-w-lg flex-col items-center gap-6 rounded-lg border border-dashed border-border p-6 text-center',
        className,
      )}
      {...props}
    />
  )
}

function EmptyStateIcon({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="empty-state-icon"
      className={cn(
        'flex size-12 shrink-0 items-center justify-center rounded-md border border-border bg-card text-foreground shadow-xs',
        '[&_svg]:size-6 [&_svg]:shrink-0 [&_svg]:text-foreground',
        className,
      )}
      {...props}
    />
  )
}

function EmptyStateTitle({ className, ...props }: React.ComponentProps<'h2'>) {
  return (
    <h2
      data-slot="empty-state-title"
      className={cn('text-xl font-semibold tracking-tight text-foreground', className)}
      {...props}
    />
  )
}

function EmptyStateDescription({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p
      data-slot="empty-state-description"
      className={cn('text-sm text-muted-foreground', className)}
      {...props}
    />
  )
}

function EmptyStateHeader({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="empty-state-header"
      className={cn('flex w-full flex-col items-center gap-2', className)}
      {...props}
    />
  )
}

function EmptyStateActions({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="empty-state-actions"
      className={cn(
        'flex w-full flex-col items-stretch justify-center gap-3 sm:flex-row sm:items-center sm:justify-center',
        className,
      )}
      {...props}
    />
  )
}

export {
  EmptyState,
  EmptyStateIcon,
  EmptyStateHeader,
  EmptyStateTitle,
  EmptyStateDescription,
  EmptyStateActions,
}
