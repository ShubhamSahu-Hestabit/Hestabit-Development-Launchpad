'use client'

import { Menu, Search, Bell, User, ChevronDown } from 'lucide-react'

export default function Navbar({ toggleSidebar }) {
  return (
    <header 
      className="fixed top-0 left-0 right-0 h-16 z-[10000] border-b border-gray-800 shadow-md"
      style={{ 
        display: 'flex', 
        alignItems: 'center', 
        backgroundColor: '#212529',
        width: '100%',
        left: 0,
        right: 0,
        padding: 0, // Remove default padding here to let the brand box touch the edge
        boxSizing: 'border-box'
      }}
    >
      
      {/* 1. BRAND SECTION (Matched to Sidebar Width) */}
      <div style={{ 
        width: '225px',       // Exact width of your sidebar
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        paddingLeft: '24px',  // Padding for the text
        flexShrink: 0         // Prevents the box from squishing
      }}>
        <span style={{ 
          color: 'white', 
          fontWeight: 'bold', 
          fontSize: '18px', 
          whiteSpace: 'nowrap',
          letterSpacing: '0.5px'
        }}>
          Hesta Analytics
        </span>
      </div>

      {/* 2. TOGGLE BUTTON (Placed right next to the brand) */}
      <button
        onClick={toggleSidebar}
        style={{ 
          background: 'transparent', 
          border: 'none', 
          color: '#adb5bd', 
          cursor: 'pointer', 
          display: 'flex', 
          alignItems: 'center',
          padding: '0 10px',
          marginLeft: '10px' // Space between text and hamburger
        }}
      >
        <Menu size={24} />
      </button>

      {/* 3. RIGHT SECTION (Search & Profile pushed to the far right) */}
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '24px', 
        marginLeft: 'auto', // This pushes everything after the hamburger to the right
        paddingRight: '24px' 
      }}>
        
        {/* Search Bar */}
        <div className="hidden md:flex" style={{ display: 'flex' }}>
          <input 
            placeholder="Search for..." 
            style={{ 
              backgroundColor: 'white', 
              border: 'none', 
              padding: '8px 12px', 
              borderRadius: '4px 0 0 4px', 
              width: '256px', 
              outline: 'none',
              fontSize: '14px'
            }}
          />
          <button style={{ backgroundColor: '#0d6efd', color: 'white', border: 'none', padding: '0 16px', borderRadius: '0 4px 4px 0', cursor: 'pointer' }}>
            <Search size={18} />
          </button>
        </div>

        {/* Profile Icons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', color: '#adb5bd' }}>
          <Bell size={20} style={{ cursor: 'pointer' }} />
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <div style={{ width: '32px', height: '32px', backgroundColor: '#6c757d', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
               <User size={18} color="white" />
            </div>
            <ChevronDown size={14} />
          </div>
        </div>
      </div>
    </header>
  );
}