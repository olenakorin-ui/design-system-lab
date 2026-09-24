import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'
import { MoreHorizontal } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const meta = {
  title: 'Components/Table',
  component: Table,
  parameters: { layout: 'padded' },
  tags: ['autodocs'],
} satisfies Meta<typeof Table>

export default meta
type Story = StoryObj<typeof meta>

const SAMPLE = [
  { id: '1', name: 'Alex Morgan', email: 'alex.morgan@example.com', role: 'Admin', status: 'Active' },
  { id: '2', name: 'Jordan Lee', email: 'jordan.lee@example.com', role: 'Editor', status: 'Active' },
  { id: '3', name: 'Sam Rivera', email: 'sam.rivera@example.com', role: 'Viewer', status: 'Inactive' },
]

export const Default: Story = {
  render: () => (
    <Table>
      <TableCaption>A list of users in the directory.</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Role</TableHead>
          <TableHead className="text-right">Status</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {SAMPLE.map((row) => (
          <TableRow key={row.id}>
            <TableCell className="font-medium">{row.name}</TableCell>
            <TableCell>{row.email}</TableCell>
            <TableCell>{row.role}</TableCell>
            <TableCell className="text-right">
              <Badge variant={row.status === 'Active' ? 'verified' : 'outline'}>{row.status}</Badge>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={3}>Total</TableCell>
          <TableCell className="text-right">{SAMPLE.length} users</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  ),
}

export const Selectable: Story = {
  render: () => {
    const [selected, setSelected] = useState<string[]>([])
    const allSelected = SAMPLE.every((r) => selected.includes(r.id))
    const someSelected = SAMPLE.some((r) => selected.includes(r.id))
    return (
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-10">
              <Checkbox
                checked={allSelected ? true : someSelected ? 'indeterminate' : false}
                onCheckedChange={(v) =>
                  setSelected(v === true ? SAMPLE.map((r) => r.id) : [])
                }
                aria-label="Select all"
              />
            </TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Role</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {SAMPLE.map((row) => {
            const isSelected = selected.includes(row.id)
            return (
              <TableRow key={row.id} data-state={isSelected ? 'selected' : undefined}>
                <TableCell>
                  <Checkbox
                    checked={isSelected}
                    onCheckedChange={(v) =>
                      setSelected((prev) =>
                        v === true ? [...prev, row.id] : prev.filter((id) => id !== row.id),
                      )
                    }
                    aria-label={`Select ${row.name}`}
                  />
                </TableCell>
                <TableCell className="font-medium">{row.name}</TableCell>
                <TableCell>{row.email}</TableCell>
                <TableCell>{row.role}</TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    )
  },
}

export const SelectedRows: Story = {
  render: () => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-10">
            <Checkbox checked="indeterminate" aria-label="Select all" />
          </TableHead>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead className="w-10">
            <span className="sr-only">Actions</span>
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {SAMPLE.map((row, i) => (
          <TableRow key={row.id} data-state={i < 2 ? 'selected' : undefined}>
            <TableCell>
              <Checkbox checked={i < 2} aria-label={`Select ${row.name}`} />
            </TableCell>
            <TableCell className="font-medium">{row.name}</TableCell>
            <TableCell>{row.email}</TableCell>
            <TableCell>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" aria-label={`Actions for ${row.name}`}>
                    <MoreHorizontal />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>View</DropdownMenuItem>
                  <DropdownMenuItem>Edit</DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem variant="destructive">Deactivate</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  ),
}

export const LongContent: Story = {
  render: () => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell className="max-w-[200px] whitespace-normal break-words font-medium">
            Alexandra Montgomery-Cartwright III
          </TableCell>
          <TableCell className="max-w-[280px] whitespace-normal break-all">
            alexandra.montgomery-cartwright.operations.emea@long-enterprise-domain.example.com
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  ),
}

export const ManyRows: Story = {
  render: () => (
    <Table>
      <TableCaption>Stress test with many rows (foundation only — no virtualisation).</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Array.from({ length: 40 }, (_, i) => (
          <TableRow key={i}>
            <TableCell>{i + 1}</TableCell>
            <TableCell>User {i + 1}</TableCell>
            <TableCell>user.{i + 1}@example.com</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  ),
}

export const Empty: Story = {
  render: () => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell colSpan={2} className="h-24 text-center text-muted-foreground">
            No results.
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  ),
}

export const NarrowViewport: Story = {
  parameters: { viewport: { defaultViewport: 'mobile1' } },
  render: () => {
    const [selected, setSelected] = useState<string[]>(['1'])
    const rows = [
      ...SAMPLE,
      {
        id: '4',
        name: 'Christopher Montgomery-Whitfield III',
        email: 'christopher.montgomery.whitfield@enterprise-long-domain.example.com',
        role: 'Editor',
        status: 'Active',
      },
    ]
    return (
      <Table>
        <TableCaption>
          Narrow viewport: horizontal scroll (D009). Selection and row actions stay reachable inside
          the scrollport; no stacked cards or hidden columns.
        </TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-10">
              <Checkbox
                checked={
                  rows.every((r) => selected.includes(r.id))
                    ? true
                    : selected.length
                      ? 'indeterminate'
                      : false
                }
                onCheckedChange={(v) =>
                  setSelected(v === true ? rows.map((r) => r.id) : [])
                }
                aria-label="Select all"
              />
            </TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Role</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="w-12">
              <span className="sr-only">Actions</span>
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => {
            const isSelected = selected.includes(row.id)
            return (
              <TableRow key={row.id} data-state={isSelected ? 'selected' : undefined}>
                <TableCell>
                  <Checkbox
                    checked={isSelected}
                    onCheckedChange={(v) =>
                      setSelected((prev) =>
                        v === true ? [...prev, row.id] : prev.filter((id) => id !== row.id),
                      )
                    }
                    aria-label={`Select ${row.name}`}
                  />
                </TableCell>
                <TableCell className="font-medium whitespace-nowrap">{row.name}</TableCell>
                <TableCell className="whitespace-nowrap">{row.email}</TableCell>
                <TableCell>{row.role}</TableCell>
                <TableCell>
                  <Badge variant={row.status === 'Active' ? 'verified' : 'outline'}>
                    {row.status}
                  </Badge>
                </TableCell>
                <TableCell>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" aria-label={`Actions for ${row.name}`}>
                        <MoreHorizontal />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Edit</DropdownMenuItem>
                      <DropdownMenuItem>View</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem variant="destructive">Remove</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    )
  },
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {SAMPLE.slice(0, 2).map((row) => (
          <TableRow key={row.id}>
            <TableCell>{row.name}</TableCell>
            <TableCell>{row.email}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  ),
}
