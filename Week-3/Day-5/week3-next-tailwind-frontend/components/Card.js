'use client'

import { ArrowRight } from 'lucide-react'

export default function Card({ title, color }) {
  const colorStyles = {
    primary: '#007bff',
    warning: '#ffc107',
    success: '#28a745',
    danger: '#dc3545',
  }

  return (
    <div 
      style={{ 
        backgroundColor: colorStyles[color],
        padding: '1.25rem',
        borderRadius: '0.5rem',
        boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
        color: 'white',
        minHeight: '120px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        cursor: 'pointer',
        transition: 'box-shadow 0.2s'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.boxShadow = '0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)'
      }}
    >
      <h3 style={{ 
        fontSize: '1.125rem', 
        fontWeight: 'bold', 
        marginBottom: '0.5rem',
        color: 'white'
      }}>
        {title}
      </h3>
      <a 
        href="#" 
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.25rem',
          fontSize: '0.875rem',
          color: 'white',
          textDecoration: 'none',
          marginTop: '0.5rem'
        }}
        onClick={(e) => e.preventDefault()}
      >
        View Details
        <ArrowRight size={14} />
      </a>
    </div>
  )
}