import * as React from 'react'

import { cn } from '@/lib/utils'

/**
 * Decorative loading placeholder. Keep aria on a wrapping container (`aria-busy`,
 * `aria-live`) rather than on each skeleton bar.
 */
function Skeleton({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="skeleton"
      aria-hidden="true"
      className={cn('animate-pulse rounded-md bg-accent', className)}
      {...props}
    />
  )
}

export { Skeleton }
