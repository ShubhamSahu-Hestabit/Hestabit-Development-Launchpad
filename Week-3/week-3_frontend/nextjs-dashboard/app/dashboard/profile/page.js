'use client'

export default function ProfilePage() {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#f6f7fb',
        padding: '120px 16px 40px',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      {/* Container */}
      <div
        style={{
          maxWidth: '1100px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: '320px 1fr',
          gap: '32px',
        }}
      >
        {/* LEFT PROFILE CARD */}
        <div
          style={{
            background: '#ffffff',
            borderRadius: '16px',
            padding: '28px',
            boxShadow: '0 20px 40px rgba(0,0,0,0.06)',
            textAlign: 'center',
          }}
        >
          {/* Avatar */}
          <div
            style={{
              width: '120px',
              height: '120px',
              borderRadius: '50%',
              background: '#e5e7eb',
              margin: '0 auto 16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '40px',
              fontWeight: 700,
              color: '#6b7280',
            }}
          >
            SS
          </div>

          <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#111827' }}>
            Shubham Sahu
          </h2>
          <p style={{ color: '#6b7280', fontSize: '14px', marginTop: '4px' }}>
            Frontend Developer
          </p>

          {/* Stats */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: '24px',
              borderTop: '1px solid #e5e7eb',
              paddingTop: '16px',
            }}
          >
            {[
              { label: 'Projects', value: '24' },
              { label: 'Tasks', value: '112' },
              { label: 'Teams', value: '6' },
            ].map((item, i) => (
              <div key={i}>
                <div
                  style={{
                    fontWeight: 700,
                    color: '#111827',
                    fontSize: '16px',
                  }}
                >
                  {item.value}
                </div>
                <div style={{ fontSize: '12px', color: '#6b7280' }}>
                  {item.label}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT DETAILS CARD */}
        <div
          style={{
            background: '#ffffff',
            borderRadius: '16px',
            padding: '32px',
            boxShadow: '0 20px 40px rgba(0,0,0,0.06)',
          }}
        >
          {/* Header */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '28px',
            }}
          >
            <h3 style={{ fontSize: '20px', fontWeight: 700 }}>
              Profile Information
            </h3>
            <button
              style={{
                background: '#6366f1',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                padding: '10px 20px',
                fontSize: '13px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Edit Profile
            </button>
          </div>

          {/* Info Grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '24px',
            }}
          >
            {[
              { label: 'Full Name', value: 'Shubham Sahu' },
              { label: 'Email', value: 'shubham@gmail.com' },
              { label: 'Phone', value: '+91 9XXXXXXXXX' },
              { label: 'Role', value: 'ML Engineer' },
              { label: 'Location', value: 'India' },
              { label: 'Company', value: 'Hesta Analytics' },
            ].map((item, i) => (
              <div key={i}>
                <div
                  style={{
                    fontSize: '12px',
                    color: '#6b7280',
                    marginBottom: '4px',
                  }}
                >
                  {item.label}
                </div>
                <div
                  style={{
                    fontSize: '14px',
                    fontWeight: 600,
                    color: '#111827',
                  }}
                >
                  {item.value}
                </div>
              </div>
            ))}
          </div>

          {/* Bio */}
          <div style={{ marginTop: '32px' }}>
            <div
              style={{
                fontSize: '12px',
                color: '#6b7280',
                marginBottom: '6px',
              }}
            >
              Bio
            </div>
            <p
              style={{
                fontSize: '14px',
                color: '#374151',
                lineHeight: 1.6,
              }}
            >
              Passionate ML Engineer with a strong focus on building clean dashboards with AI integration and features.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
