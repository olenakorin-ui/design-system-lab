import * as React from 'react'

import { cn } from '@/lib/utils'

type InputProps = React.ComponentProps<'input'> & {
  /**
   * Maps Figma State=Error / Error (Focus).
   * Sets `aria-invalid` and destructive border / focus ring.
   */
  invalid?: boolean
}

function Input({ className, type = 'text', invalid = false, disabled, ...props }: InputProps) {
  return (
    <input
      type={type}
      data-slot="input"
      data-invalid={invalid ? '' : undefined}
      aria-invalid={invalid || undefined}
      disabled={disabled}
      className={cn(
        // Figma Input field chrome (Default Variant)
        'flex h-9 w-full min-w-0 rounded-md border border-input bg-[var(--custom-background-dark-input-30)]',
        'px-3 py-1 text-sm text-foreground shadow-xs',
        'placeholder:text-muted-foreground',
        'outline-none transition-[color,box-shadow,border-color,opacity]',
        'file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground',
        'disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50',
        // Focus (Figma State=Focus): border ring + custom/outline
        'focus-visible:border-ring focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]',
        // Error (Figma State=Error / Error Focus)
        'aria-invalid:border-destructive',
        'aria-invalid:focus-visible:border-destructive',
        'aria-invalid:focus-visible:shadow-[0_0_0_3px_var(--custom-destructive-20-dark-40)]',
        className,
      )}
      {...props}
    />
  )
}

export { Input }
export type { InputProps }
