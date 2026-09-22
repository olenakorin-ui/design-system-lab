import type { Meta, StoryObj } from '@storybook/react-vite'

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const meta = {
  title: 'Components/Tabs',
  component: Tabs,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
} satisfies Meta<typeof Tabs>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <Tabs defaultValue="account" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="account">Account</TabsTrigger>
        <TabsTrigger value="password">Password</TabsTrigger>
      </TabsList>
      <TabsContent value="account" className="rounded-md border border-border p-4 text-sm">
        Make changes to your account here.
      </TabsContent>
      <TabsContent value="password" className="rounded-md border border-border p-4 text-sm">
        Change your password here.
      </TabsContent>
    </Tabs>
  ),
}

export const ManyTabs: Story = {
  render: () => (
    <Tabs defaultValue="t1" className="w-[520px]">
      <TabsList>
        {['One', 'Two', 'Three', 'Four', 'Five'].map((label, i) => (
          <TabsTrigger key={label} value={`t${i + 1}`}>
            {label}
          </TabsTrigger>
        ))}
      </TabsList>
      <TabsContent value="t1" className="p-3 text-sm text-muted-foreground">
        Panel one
      </TabsContent>
    </Tabs>
  ),
}

export const LongLabels: Story = {
  render: () => (
    <Tabs defaultValue="billing" className="w-[520px]">
      <TabsList>
        <TabsTrigger value="billing">Billing preferences</TabsTrigger>
        <TabsTrigger value="notifications">Notification settings</TabsTrigger>
      </TabsList>
      <TabsContent value="billing" className="p-3 text-sm">
        Long label tab content.
      </TabsContent>
      <TabsContent value="notifications" className="p-3 text-sm">
        Notifications content.
      </TabsContent>
    </Tabs>
  ),
}

export const DisabledTab: Story = {
  render: () => (
    <Tabs defaultValue="active" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="active">Active</TabsTrigger>
        <TabsTrigger value="disabled" disabled>
          Disabled
        </TabsTrigger>
        <TabsTrigger value="other">Other</TabsTrigger>
      </TabsList>
      <TabsContent value="active" className="p-3 text-sm">
        Active panel
      </TabsContent>
    </Tabs>
  ),
}

export const FocusVisible: Story = {
  render: () => (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-muted-foreground">Tab into the list, then use arrows.</p>
      <Tabs defaultValue="a" className="w-[360px]">
        <TabsList>
          <TabsTrigger value="a">First</TabsTrigger>
          <TabsTrigger value="b">Second</TabsTrigger>
          <TabsTrigger value="c">Third</TabsTrigger>
        </TabsList>
        <TabsContent value="a" className="p-3 text-sm">
          First panel
        </TabsContent>
      </Tabs>
    </div>
  ),
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <Tabs defaultValue="account" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="account">Account</TabsTrigger>
        <TabsTrigger value="password">Password</TabsTrigger>
      </TabsList>
      <TabsContent value="account" className="rounded-md border border-border p-4 text-sm">
        Dark mode tabs.
      </TabsContent>
    </Tabs>
  ),
}
