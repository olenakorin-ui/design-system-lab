import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { LoaderCircle } from 'lucide-react'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
  [
    'inline-flex items-center justify-center gap-2 whitespace-nowrap',
    'rounded-md text-sm font-medium',
    'transition-[color,background-color,box-shadow,opacity,border-color]',
    'disabled:pointer-events-none disabled:opacity-50',
    '[&_svg]:pointer-events-none [&_svg:not([class*=\'size-\'])]:size-4 [&_svg]:shrink-0',
    'outline-none focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]',
  ].join(' '),
  {
    variants: {
      variant: {
        default: [
          'bg-primary text-primary-foreground shadow-xs',
          // Figma Hover: primary + alpha/90 overlay
          'hover:[background-image:linear-gradient(var(--alpha-90),var(--alpha-90))]',
          'active:opacity-60',
        ].join(' '),
        secondary: [
          'bg-secondary text-secondary-foreground shadow-xs',
          // Figma Hover: stacked base/secondary + alpha/80 @ paint opacity 0.2.
          // No dedicated Mode hover recipe — approximate (see docs/components/button.md).
          'hover:[background-image:linear-gradient(color-mix(in_srgb,var(--alpha-80)_20%,transparent),color-mix(in_srgb,var(--alpha-80)_20%,transparent))]',
          'active:opacity-60',
        ].join(' '),
        destructive: [
          'bg-[var(--custom-destructive-dark-60)] text-destructive-foreground shadow-xs',
          'hover:bg-[var(--custom-destructive-dark-90)]',
          'focus-visible:shadow-[0_0_0_3px_var(--custom-destructive-20-dark-40)]',
          'active:opacity-60',
        ].join(' '),
        outline: [
          'border border-input bg-[var(--custom-background-dark-input-30)] text-foreground shadow-xs',
          'hover:bg-[var(--custom-accent-dark-input-50)] hover:text-accent-foreground',
          'focus-visible:border-ring',
          'active:opacity-60',
        ].join(' '),
        ghost: [
          'bg-transparent text-foreground',
          'hover:bg-accent hover:text-accent-foreground',
          'active:opacity-60',
        ].join(' '),
        link: [
          // Figma Link Hover uses textDecoration UNDERLINE; Default/Pressed do not.
          'bg-transparent text-primary underline-offset-4',
          'hover:underline',
          'active:opacity-60',
        ].join(' '),
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 px-3',
        lg: 'h-10 px-8',
        icon: 'size-9',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
)

type ButtonProps = React.ComponentProps<'button'> &
  VariantProps<typeof buttonVariants> & {
    /**
     * Render as Radix Slot. **Unsupported with `loading`** — use a real `<button>` when loading.
     */
    asChild?: boolean
    loading?: boolean
  }

function Button({
  className,
  variant,
  size,
  asChild = false,
  loading = false,
  disabled,
  children,
  ...props
}: ButtonProps) {
  // asChild + loading is unsupported: Slot expects a single child and cannot host the spinner chrome.
  const useSlot = asChild && !loading
  const Comp = useSlot ? Slot : 'button'
  const isDisabled = Boolean(disabled || loading)

  return (
    <Comp
      data-slot="button"
      data-loading={loading ? '' : undefined}
      className={cn(
        buttonVariants({ variant, size }),
        loading && 'opacity-50',
        className,
      )}
      disabled={useSlot ? undefined : isDisabled}
      aria-disabled={useSlot ? isDisabled || undefined : undefined}
      aria-busy={loading || undefined}
      {...props}
    >
      {loading ? (
        <>
          <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
          {size === 'icon' ? <span className="sr-only">Loading</span> : children}
        </>
      ) : (
        children
      )}
    </Comp>
  )
}

export { Button, buttonVariants }
export type { ButtonProps }
