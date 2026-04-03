'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  Home,
  Layout,
  FileText,
  BarChart3,
  Table,
  ChevronRight
} from 'lucide-react'
import { useState } from 'react'

export default function Sidebar({ isOpen }) {
  const pathname = usePathname()
  const [layoutsOpen, setLayoutsOpen] = useState(false)
  const [pagesOpen, setPagesOpen] = useState(false)

  const isActive = (href) => pathname === href

  // Inline Style Helper
  const getLinkStyle = (href) => ({
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '12px 24px',
    fontSize: '14px',
    textDecoration: 'none',
    transition: '0.2s',
    color: 'white', // FORCES TEXT WHITE
    backgroundColor: isActive(href) ? '#0d6efd' : 'transparent',
    fontWeight: isActive(href) ? '600' : '400',
  })

  const headerStyle = {
    color: '#adb5bd', // Light grey for headers
    fontSize: '11px',
    fontWeight: '800',
    textTransform: 'uppercase',
    padding: '16px 24px 8px 24px',
    letterSpacing: '1px'
  }

  const buttonStyle = {
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '12px 24px',
    fontSize: '14px',
    color: 'white', // FORCES TEXT WHITE
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer'
  }

  return (
    <aside
      style={{
        fixed: 'fixed',
        top: '32px',
        left: 0,
        height: 'calc(100vh - 20px)',
        width: '225px',
        backgroundColor: '#212529',
        zIndex: 40,
        position: 'fixed',
        transform: isOpen ? 'translateX(0)' : 'translateX(-100%)',
        transition: 'transform 0.3s ease-in-out',
        borderRight: '1px solid #343a40'
      }}
    >
      {/* CORE SECTION */}
      <div>
        <div style={headerStyle}>Core</div>
        <Link href="/dashboard" style={getLinkStyle('/dashboard')}>
          <Home size={16} color="white" />
          Dashboard
        </Link>
      </div>

      {/* INTERFACE SECTION */}
      <div>
        <div style={headerStyle}>Interface</div>

        <button onClick={() => setLayoutsOpen(!layoutsOpen)} style={buttonStyle}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Layout size={16} color="white" />
            Layouts
          </div>
          <ChevronRight
            size={14}
            style={{ transform: layoutsOpen ? 'rotate(90deg)' : 'rotate(0deg)', transition: '0.2s' }}
            color="white"
          />
        </button>

        <button onClick={() => setPagesOpen(!pagesOpen)} style={buttonStyle}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <FileText size={16} color="white" />
            Pages
          </div>
          <ChevronRight
            size={14}
            style={{ transform: pagesOpen ? 'rotate(90deg)' : 'rotate(0deg)', transition: '0.2s' }}
            color="white"
          />
        </button>
      </div>

      {/* ADDONS SECTION */}
      <div>
        <div style={headerStyle}>Addons</div>

        <Link href="/dashboard/charts" style={getLinkStyle('/dashboard/charts')}>
          <BarChart3 size={16} color="white" />
          Charts
        </Link>

        <Link href="/dashboard/tables" style={getLinkStyle('/dashboard/tables')}>
          <Table size={16} color="white" />
          Tables
        </Link>
      </div>
    </aside>
  )
}