import { Button } from '@/components/ui/button'

export default function App() {
  return (
    <main className="flex min-h-screen flex-col items-start gap-6 p-8">
      <h1 className="text-2xl font-medium">Design System Lab</h1>
      <p className="text-muted-foreground text-sm">
        Pipeline check: tokens → semantic CSS → shadcn Button → React.
      </p>
      <div className="flex flex-wrap gap-3">
        <Button>Default</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="outline">Outline</Button>
        <Button loading>Loading</Button>
      </div>
    </main>
  )
}
