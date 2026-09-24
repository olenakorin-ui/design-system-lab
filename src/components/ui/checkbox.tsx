import * as React from 'react'
import * as CheckboxPrimitive from '@radix-ui/react-checkbox'
import { Check, Minus } from 'lucide-react'

import { cn } from '@/lib/utils'

type CheckboxProps = React.ComponentProps<typeof CheckboxPrimitive.Root>

function Checkbox({ className, ...props }: CheckboxProps) {
  return (
    <CheckboxPrimitive.Root
      data-slot="checkbox"
      className={cn(
        // Figma Checkbox box — 16×16, radius 4px
        'peer size-4 shrink-0 rounded-[4px] border shadow-xs outline-none',
        'border-input bg-[var(--custom-background-dark-input-30)]',
        'transition-[color,box-shadow,background-color,border-color,opacity]',
        // Active (checked) + Indeterminate (code extension; Figma Status axis is Active/Inactive only)
        'data-[state=checked]:border-primary data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground',
        'data-[state=indeterminate]:border-primary data-[state=indeterminate]:bg-primary data-[state=indeterminate]:text-primary-foreground',
        // Focus
        'focus-visible:border-ring focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]',
        // Pressed
        'active:opacity-60',
        // Disabled
        'disabled:cursor-not-allowed disabled:opacity-50',
        className,
      )}
      {...props}
    >
      <CheckboxPrimitive.Indicator
        data-slot="checkbox-indicator"
        className="flex items-center justify-center text-current"
      >
        <Check
          data-icon="check"
          className="size-3.5 [[data-slot=checkbox][data-state=indeterminate]_&]:hidden"
          strokeWidth={3}
          aria-hidden="true"
        />
        <Minus
          data-icon="minus"
          className="hidden size-3.5 [[data-slot=checkbox][data-state=indeterminate]_&]:block"
          strokeWidth={3}
          aria-hidden="true"
        />
      </CheckboxPrimitive.Indicator>
    </CheckboxPrimitive.Root>
  )
}

export { Checkbox }
export type { CheckboxProps }
