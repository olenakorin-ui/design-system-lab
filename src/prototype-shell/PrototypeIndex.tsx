import { useEffect, useState } from 'react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

import {
  experimentOutcomes,
  feedbackLoop,
  showcaseMetrics,
  showcasePrototypes,
  systemPipeline,
} from './showcase-content'
import {
  AUTHOR_NAME,
  AUTHOR_ROLE,
  CASE_STUDY_HREF,
  SOCIAL_LINKS,
} from './site-config'

export type PrototypeIndexProps = {
  onOpen: (route: string) => void
  theme: 'light' | 'dark'
  onThemeChange: (theme: 'light' | 'dark') => void
}

function ThemeToggle({
  theme,
  onThemeChange,
}: {
  theme: 'light' | 'dark'
  onThemeChange: (theme: 'light' | 'dark') => void
}) {
  return (
    <div className="flex items-center gap-1" role="group" aria-label="Color theme">
      <Button
        type="button"
        size="sm"
        variant={theme === 'light' ? 'secondary' : 'outline'}
        onClick={() => onThemeChange('light')}
        aria-pressed={theme === 'light'}
      >
        Light
      </Button>
      <Button
        type="button"
        size="sm"
        variant={theme === 'dark' ? 'secondary' : 'outline'}
        onClick={() => onThemeChange('dark')}
        aria-pressed={theme === 'dark'}
      >
        Dark
      </Button>
    </div>
  )
}

function ProcessFlow({ items }: { items: readonly string[] }) {
  return (
    <ol
      className="flex flex-col gap-3 md:flex-row md:flex-wrap md:items-center md:gap-x-2 md:gap-y-3"
      aria-label="System workflow"
    >
      {items.map((item, index) => (
        <li key={item} className="flex flex-col gap-3 md:flex-row md:items-center md:gap-2">
          <span className="border border-border bg-card px-4 py-3 text-sm font-medium text-card-foreground md:px-3 md:py-2">
            {item}
          </span>
          {index < items.length - 1 ? (
            <>
              <span className="px-1 text-muted-foreground md:hidden" aria-hidden="true">
                ↓
              </span>
              <span className="hidden text-muted-foreground md:inline" aria-hidden="true">
                →
              </span>
            </>
          ) : null}
        </li>
      ))}
    </ol>
  )
}

function FeedbackFlow({ items }: { items: readonly string[] }) {
  return (
    <ol
      className="flex flex-col gap-3 md:flex-row md:flex-wrap md:items-baseline md:gap-x-1 md:gap-y-2"
      aria-label="Evidence feedback loop"
    >
      {items.map((item, index) => (
        <li key={item} className="flex flex-col gap-3 md:flex-row md:items-baseline md:gap-1">
          <span className="text-sm font-medium text-foreground">{item}</span>
          {index < items.length - 1 ? (
            <>
              <span className="text-muted-foreground md:hidden" aria-hidden="true">
                ↓
              </span>
              <span className="hidden text-muted-foreground md:inline" aria-hidden="true">
                →
              </span>
            </>
          ) : null}
        </li>
      ))}
    </ol>
  )
}

function SocialPlaceholder({
  label,
  href,
}: {
  label: string
  href: string | null
}) {
  if (href) {
    return (
      <a
        href={href}
        className="text-sm text-foreground underline-offset-4 outline-none hover:underline focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]"
        rel="noopener noreferrer"
        target="_blank"
      >
        {label}
      </a>
    )
  }

  return (
    <span className="text-sm text-muted-foreground" title={`${label} URL pending`}>
      {label}
    </span>
  )
}

export function PrototypeIndex({ onOpen, theme, onThemeChange }: PrototypeIndexProps) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-background focus:px-3 focus:py-2 focus:text-sm focus:shadow-[0_0_0_3px_var(--custom-outline)]"
      >
        Skip to content
      </a>

      <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between gap-4 px-4 py-3 sm:px-8">
          <div className="min-w-0">
            <p className="text-sm font-semibold tracking-tight text-foreground">OK</p>
            <p className="truncate text-xs text-muted-foreground">Prototype Lab</p>
          </div>
          <nav aria-label="Page" className="hidden items-center gap-6 sm:flex">
            <a
              href="#prototypes"
              className="text-sm text-muted-foreground outline-none hover:text-foreground focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]"
            >
              Prototypes
            </a>
            <a
              href="#process"
              className="text-sm text-muted-foreground outline-none hover:text-foreground focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]"
            >
              Process
            </a>
            <a
              href="#about"
              className="text-sm text-muted-foreground outline-none hover:text-foreground focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]"
            >
              About
            </a>
          </nav>
          <ThemeToggle theme={theme} onThemeChange={onThemeChange} />
        </div>
        {/* Mobile anchor row — no hamburger menu in v1 */}
        <nav
          aria-label="Page sections"
          className="flex gap-4 overflow-x-auto border-t border-border px-4 py-2 sm:hidden"
        >
          <a href="#prototypes" className="shrink-0 text-sm text-muted-foreground">
            Prototypes
          </a>
          <a href="#process" className="shrink-0 text-sm text-muted-foreground">
            Process
          </a>
          <a href="#about" className="shrink-0 text-sm text-muted-foreground">
            About
          </a>
        </nav>
      </header>

      <main id="main">
        {/* Hero */}
        <section
          className="border-b border-border"
          aria-labelledby="hero-heading"
        >
          <div className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-4 py-16 sm:px-8 sm:py-24">
            <div className="flex max-w-3xl flex-col gap-5">
              <p className="text-xs font-medium tracking-[0.14em] text-muted-foreground uppercase">
                AI-powered product design · Design systems
              </p>
              <h1
                id="hero-heading"
                className="text-3xl font-semibold tracking-tight text-balance text-foreground sm:text-4xl md:text-5xl"
              >
                From design system to working product prototypes.
              </h1>
              <p className="max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
                A public lab for testing how a structured Figma design system can translate
                into reusable React components, AI-assisted product workflows, and measurable
                production prototypes.
              </p>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <Button asChild className="w-full sm:w-auto">
                  <a href="#prototypes">Explore prototypes</a>
                </Button>
                <Button asChild variant="outline" className="w-full sm:w-auto">
                  <a href={CASE_STUDY_HREF}>Read the case study</a>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Outcome metrics */}
        <section
          className="border-b border-border"
          aria-label="Outcome metrics"
        >
          <div className="mx-auto grid w-full max-w-5xl grid-cols-2 gap-px bg-border lg:grid-cols-4">
            {showcaseMetrics.map((metric) => (
              <div
                key={metric.label}
                className="flex flex-col gap-2 bg-background px-4 py-8 sm:px-8"
              >
                <p className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
                  {metric.value}
                </p>
                <p className="text-sm text-muted-foreground">{metric.label}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Prototypes */}
        <section
          id="prototypes"
          className="border-b border-border scroll-mt-24"
          aria-labelledby="prototypes-heading"
        >
          <div className="mx-auto flex w-full max-w-5xl flex-col gap-10 px-4 py-16 sm:px-8 sm:py-20">
            <div className="flex max-w-2xl flex-col gap-3">
              <h2
                id="prototypes-heading"
                className="text-2xl font-semibold tracking-tight text-foreground sm:text-3xl"
              >
                Explore the prototypes
              </h2>
              <p className="text-base leading-relaxed text-muted-foreground">
                Each workflow was used to stress-test the design system, expose missing
                patterns, and validate improvements in a real interactive interface.
              </p>
            </div>

            <ul className="grid grid-cols-1 gap-6 md:grid-cols-2">
              {showcasePrototypes.map((prototype) => (
                <li
                  key={prototype.id}
                  className="flex flex-col gap-5 border border-border p-5 sm:p-6"
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-lg font-semibold text-foreground">{prototype.name}</h3>
                    <Badge variant="verified">{prototype.status}</Badge>
                  </div>
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {prototype.description}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {prototype.metadata.join(' · ')}
                  </p>
                  <ul className="flex flex-wrap gap-2" aria-label={`${prototype.name} capabilities`}>
                    {prototype.capabilities.map((cap) => (
                      <li key={cap}>
                        <Badge variant="outline">{cap}</Badge>
                      </li>
                    ))}
                  </ul>
                  <div className="mt-auto pt-2">
                    <Button
                      type="button"
                      className="w-full sm:w-auto"
                      onClick={() => onOpen(prototype.route)}
                    >
                      {prototype.cta}
                    </Button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Process */}
        <section
          id="process"
          className="border-b border-border scroll-mt-24"
          aria-labelledby="process-heading"
        >
          <div className="mx-auto flex w-full max-w-5xl flex-col gap-10 px-4 py-16 sm:px-8 sm:py-20">
            <h2
              id="process-heading"
              className="max-w-2xl text-2xl font-semibold tracking-tight text-foreground sm:text-3xl"
            >
              A design system built through real product use
            </h2>

            <div className="flex flex-col gap-4">
              <h3 className="text-sm font-medium tracking-wide text-muted-foreground uppercase">
                System pipeline
              </h3>
              <ProcessFlow items={systemPipeline} />
            </div>

            <div className="flex flex-col gap-4 border-t border-border pt-8">
              <h3 className="text-sm font-medium tracking-wide text-muted-foreground uppercase">
                Evidence loop
              </h3>
              <FeedbackFlow items={feedbackLoop} />
            </div>
          </div>
        </section>

        {/* Outcomes */}
        <section
          className="border-b border-border"
          aria-labelledby="outcomes-heading"
        >
          <div className="mx-auto flex w-full max-w-5xl flex-col gap-10 px-4 py-16 sm:px-8 sm:py-20">
            <h2
              id="outcomes-heading"
              className="text-2xl font-semibold tracking-tight text-foreground sm:text-3xl"
            >
              What the experiments proved
            </h2>
            <ul className="grid grid-cols-1 gap-8 sm:grid-cols-2">
              {experimentOutcomes.map((outcome) => (
                <li key={outcome.title} className="flex flex-col gap-2 border-t border-border pt-4">
                  <h3 className="text-base font-semibold text-foreground">{outcome.title}</h3>
                  <p className="text-sm leading-relaxed text-muted-foreground">{outcome.body}</p>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* About */}
        <section
          id="about"
          className="border-b border-border scroll-mt-24"
          aria-labelledby="about-heading"
        >
          <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-16 sm:px-8 sm:py-20">
            <h2
              id="about-heading"
              className="text-2xl font-semibold tracking-tight text-foreground sm:text-3xl"
            >
              About this project
            </h2>
            <p className="max-w-2xl text-base leading-relaxed text-muted-foreground">
              Prototype Lab is an independent product-design experiment exploring how Figma,
              design tokens, React, Storybook, Cursor, GitHub, and AI-assisted workflows can
              operate as one reusable system.
            </p>
            <p className="max-w-2xl text-sm leading-relaxed text-muted-foreground">
              All product workflows, people, organizations, and data shown in the prototypes
              are fictional and created for demonstration purposes.
            </p>
          </div>
        </section>
      </main>

      <footer className="border-t border-border">
        <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-4 py-10 sm:flex-row sm:items-end sm:justify-between sm:px-8">
          <div className="flex flex-col gap-1">
            <p className="text-sm font-semibold text-foreground">{AUTHOR_NAME}</p>
            <p className="text-sm text-muted-foreground">{AUTHOR_ROLE}</p>
          </div>
          <nav aria-label="Author links" className="flex flex-wrap gap-4">
            <SocialPlaceholder label="Portfolio" href={SOCIAL_LINKS.portfolio} />
            <SocialPlaceholder label="LinkedIn" href={SOCIAL_LINKS.linkedin} />
            <SocialPlaceholder label="GitHub" href={SOCIAL_LINKS.github} />
          </nav>
        </div>
      </footer>
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
