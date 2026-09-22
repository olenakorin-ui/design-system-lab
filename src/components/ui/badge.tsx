import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const badgeVariants = cva(
  [
    'inline-flex items-center justify-center gap-1 whitespace-nowrap',
    'rounded-md border px-2 py-0.5 text-xs font-semibold',
    'w-fit shrink-0',
    '[&_svg]:pointer-events-none [&_svg:not([class*=\'size-\'])]:size-3 [&_svg]:shrink-0',
    'transition-[color,background-color,box-shadow,border-color]',
  ].join(' '),
  {
    variants: {
      variant: {
        default: [
          'border-transparent bg-primary text-primary-foreground',
          // Figma Hover: primary + alpha/80 @ ~0.2
          'hover:[background-image:linear-gradient(color-mix(in_srgb,var(--alpha-80)_20%,transparent),color-mix(in_srgb,var(--alpha-80)_20%,transparent))]',
        ].join(' '),
        secondary: 'border-transparent bg-secondary text-secondary-foreground',
        outline: 'border-border bg-background text-foreground',
        destructive: [
          'border-transparent bg-[var(--custom-destructive-dark-60)] text-white',
          'hover:bg-[var(--custom-destructive-dark-90)]',
        ].join(' '),
        verified:
          'border-transparent bg-[var(--custom-blue-500-dark-blue-600)] text-white',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

type BadgeProps = React.ComponentProps<'span'> &
  VariantProps<typeof badgeVariants> & {
    asChild?: boolean
  }

function Badge({ className, variant, asChild = false, ...props }: BadgeProps) {
  const Comp = asChild ? Slot : 'span'
  return (
    <Comp
      data-slot="badge"
      className={cn(badgeVariants({ variant }), className)}
      {...props}
    />
  )
}

export { Badge, badgeVariants }
export type { BadgeProps }
