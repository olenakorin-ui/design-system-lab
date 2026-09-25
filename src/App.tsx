import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/react'

import { PrototypeRouter } from '@/prototype-shell/PrototypeRouter'

export default function App() {
  return (
    <>
      <PrototypeRouter />
      <Analytics />
      <SpeedInsights />
    </>
  )
}
