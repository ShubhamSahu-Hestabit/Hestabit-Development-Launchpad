'use client'

import { useState } from 'react'
import Navbar from '@/components/Navbar'
import Sidebar from '@/components/Sidebar'

export default function DashboardLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen bg-[#f8f9fc]">
      {/* FIXED NAVBAR */}
      <Navbar toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />

      {/* CONTAINER BELOW NAVBAR */}
      <div className="flex" style={{ display: 'flex', paddingTop: '64px' }}>
        
        {/* SIDEBAR */}
        <Sidebar isOpen={sidebarOpen} />

        {/* MAIN CONTENT AREA */}
        <main
          className="flex-1 transition-all duration-300"
          style={{ 
            flex: 1, 
            marginLeft: sidebarOpen ? '225px' : '0',
            transition: 'margin 0.3s ease',
            padding: '24px',
            minHeight: 'calc(100vh - 64px)'
          }}
        >
          {children}
        </main>
      </div>
    </div>
  )
}