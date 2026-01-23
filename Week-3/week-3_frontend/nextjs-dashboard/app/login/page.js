'use client'

export default function LoginPage() {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#f6f7fb',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      {/* Login Card */}
      <div
        style={{
          width: '100%',
          maxWidth: '420px',
          background: '#ffffff',
          borderRadius: '16px',
          padding: '40px 36px',
          boxShadow: '0 20px 40px rgba(0,0,0,0.08)',
        }}
      >
        {/* Title */}
        <h2
          style={{
            textAlign: 'center',
            fontSize: '26px',
            fontWeight: 700,
            marginBottom: '28px',
            color: '#111827',
          }}
        >
          Login
        </h2>

        {/* Username */}
        <div style={{ marginBottom: '18px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              border: '1px solid #d1d5db',
              borderRadius: '10px',
              padding: '12px 14px',
              gap: '10px',
            }}
          >
            <span style={{ color: '#9ca3af' }}>👤</span>
            <input
              type="text"
              placeholder="Username"
              style={{
                border: 'none',
                outline: 'none',
                width: '100%',
                fontSize: '14px',
              }}
            />
          </div>
        </div>

        {/* Password */}
        <div style={{ marginBottom: '14px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              border: '1px solid #d1d5db',
              borderRadius: '10px',
              padding: '12px 14px',
              gap: '10px',
            }}
          >
            <span style={{ color: '#9ca3af' }}>🔒</span>
            <input
              type="password"
              placeholder="Password"
              style={{
                border: 'none',
                outline: 'none',
                width: '100%',
                fontSize: '14px',
              }}
            />
          </div>
        </div>

        {/* Remember + Forgot */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '13px',
            color: '#6b7280',
            marginBottom: '26px',
          }}
        >
          <label style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <input type="checkbox" />
            Remember me
          </label>
          <span style={{ cursor: 'pointer' }}>Forgot Password?</span>
        </div>

        {/* Login Button */}
        <button
          style={{
            width: '100%',
            background: '#34d399',
            color: '#ffffff',
            border: 'none',
            borderRadius: '10px',
            padding: '14px',
            fontSize: '14px',
            fontWeight: 600,
            cursor: 'pointer',
            letterSpacing: '1px',
          }}
        >
          LOGIN
        </button>
      </div>
    </div>
  )
}
