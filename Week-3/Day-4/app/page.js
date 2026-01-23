'use client'

import Link from "next/link";
import Image from "next/image";
import { 
  Zap, 
  Shield, 
  Globe, 
  BarChart3, 
  Star 
} from "lucide-react";

export default function LandingPage() {
  const theme = {
    bg: '#050505',
    card: '#0f1115',
    accent: '#6366f1',
    textMain: '#ffffff',
    textMuted: '#94a3b8',
    border: 'rgba(255,255,255,0.1)'
  };

  return (
    <div style={{
      backgroundColor: theme.bg,
      color: theme.textMain,
      minHeight: '100vh',
      overflowX: 'hidden'
    }}>

      {/* ================= GLOBAL FIXES ================= */}
      <style jsx global>{`
        a { text-decoration: none; color: inherit; }
        .glass-card {
          background: ${theme.card};
          border: 1px solid ${theme.border};
          transition: 0.3s ease;
        }
        .glass-card:hover {
          transform: translateY(-6px);
          border-color: ${theme.accent};
        }
      `}</style>

      {/* ================= NAVBAR ================= */}
      <nav style={{
        position: 'fixed',
        top: 0,
        width: '100%',
        height: '90px',
        background: 'rgba(5,5,5,0.85)',
        backdropFilter: 'blur(10px)',
        borderBottom: `1px solid ${theme.border}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 5%',
        zIndex: 1000
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 ,fontSize: 20 }}>
          <BarChart3 color={theme.accent} />
          <strong>Hesta<span style={{ color: theme.accent }}>Analytics</span></strong>
        </div>
        <div className="hidden md:flex" style={{ display: 'flex', gap: 24, fontSize: 20 }}>
          <Link href="/">Home</Link>
          <Link href="/about">About</Link>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/login">Login</Link>
        </div>
      </nav>

      {/* ================= HERO ================= */}
      <section style={{
        paddingTop: 140,
        paddingBottom: 100,
        maxWidth: 1400,
        margin: '0 auto',
        padding: '140px 5% 100px'
      }}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-60 items-center">
          {/* LEFT CONTENT */}
          <div>
            <h1 style={{
              fontSize: 'clamp(42px, 6vw, 72px)',
              fontWeight: 900,
              marginBottom: 24,
              lineHeight: 1.1
            }}>
              Understand your <br />
              <span style={{ color: theme.accent }}>Business Data</span>
            </h1>

            <p style={{
              color: theme.textMuted,
              fontSize: 18,
              marginBottom: 32,
              lineHeight: 1.6
            }}>
              A modern analytics platform built for speed, clarity, and scale. 
              Transform raw data into actionable insights with real-time dashboards 
              and intelligent reporting.
            </p>

            {/* CTA BUTTONS */}
            <div className="flex flex-wrap md:flex-nowrap" style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
              <Link href="/dashboard" style={{
                background: theme.accent,
                padding: '14px 36px',
                borderRadius: 999,
                fontWeight: 600,
                display: 'inline-block'
              }}>
                Get Started
              </Link>
              
              <Link href="/about" style={{
                background: 'transparent',
                border: `2px solid ${theme.border}`,
                padding: '14px 36px',
                borderRadius: 999,
                fontWeight: 600,
                display: 'inline-block'
              }}>
                Learn More
              </Link>
            </div>

            {/* Feature highlights */}
            <div className="flex flex-wrap lg:flex-nowrap" style={{ marginTop: 48, display: 'flex', gap: 32, flexWrap: 'wrap' }}>
              <div>
                <div style={{ color: theme.accent, fontSize: 32, fontWeight: 700 }}>99.9%</div>
                <div style={{ color: theme.textMuted, fontSize: 14 }}>Uptime</div>
              </div>
              <div>
                <div style={{ color: theme.accent, fontSize: 32, fontWeight: 700 }}>10k+</div>
                <div style={{ color: theme.textMuted, fontSize: 14 }}>Active Users</div>
              </div>
              <div>
                <div style={{ color: theme.accent, fontSize: 32, fontWeight: 700 }}>&lt;100ms</div>
                <div style={{ color: theme.textMuted, fontSize: 14 }}>Response Time</div>
              </div>
            </div>
          </div>

          {/* RIGHT IMAGE */}
          <div style={{ position: 'relative' }}>
            <Image
              src="/dashboard-preview1.png"
              alt="Analytics dashboard preview"
              width={1200}
              height={700}
              priority
              style={{
                borderRadius: 24,
                width: '100%',
                height: 'auto',
                boxShadow: '0 40px 100px rgba(99,102,241,0.3)',
                border: `1px solid ${theme.border}`
              }}
            />
            
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '80%',
              height: '80%',
              background: `radial-gradient(circle, ${theme.accent}33 0%, transparent 70%)`,
              zIndex: -1,
              filter: 'blur(60px)'
            }} />
          </div>
        </div>
      </section>

      {/* ================= FEATURES ================= */}
      <section style={{
        maxWidth: 1200,
        margin: '0 auto',
        padding: '80px 5%'
      }}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-24">
          {[
            { icon: Zap, title: "Fast Insights", text: "Live metrics update instantly." },
            { icon: Shield, title: "Secure Data", text: "Enterprise-grade security built-in." },
            { icon: Globe, title: "Global Scale", text: "Low latency worldwide." }
          ].map((f, i) => (
            <div key={i} className="glass-card" style={{ padding: 36, borderRadius: 24 }}>
              <f.icon color={theme.accent} size={28} />
              <h3 style={{ marginTop: 16 }}>{f.title}</h3>
              <p style={{ color: theme.textMuted }}>{f.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ================= TESTIMONIALS ================= */}
      <section style={{
        padding: '80px 5%',
        textAlign: 'center'
      }}>
        <h2 style={{ fontSize: 38, fontWeight: 800, marginBottom: 16 }}>
          Loved by teams
        </h2>
        <p style={{ color: theme.textMuted, marginBottom: 60 }}>
          Trusted by founders and product teams worldwide
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-24 max-width-1100 mx-auto">
          {["Amazing UI and insights!", "Our decisions improved instantly.", "Clean, fast, reliable."].map((text, i) => (
            <div key={i} className="glass-card" style={{ padding: 32, borderRadius: 24 }}>
              <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
                {[...Array(5)].map((_, j) => (
                  <Star key={j} size={16} color="#facc15" fill="#facc15" />
                ))}
              </div>
              <p style={{ color: theme.textMuted }}>{text}</p>
              <strong style={{ display: 'block', marginTop: 16 }}>
                — Product Manager
              </strong>
            </div>
          ))}
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer style={{
        borderTop: `1px solid ${theme.border}`,
        padding: '40px 5%',
        textAlign: 'center',
        color: theme.textMuted
      }}>
        © Hesta Analytics. All rights reserved.
      </footer>
    </div>
  );
}
