'use client'
import Link from 'next/link'

export default function AboutPage() {
  return (
    <div style={styles.page}>
      {/* NAVBAR */}
      <header style={styles.nav}>
        <div style={styles.logo}>Hesta Analytics</div>
        <nav style={styles.navLinks}>
          <Link href="/" style={styles.link}>Home</Link>
          <Link href="/dashboard" style={styles.primaryLink}>Dashboard</Link>
        </nav>
      </header>

      {/* HEADER */}
      <section style={styles.header}>
        <h1 style={styles.title}>About Hesta Analytics</h1>
        <p style={styles.subtitle}>
          Hesta Anlytics is a next-generation data infrastructure platform designed to
          handle high-frequency, mission-critical data for modern enterprises.
        </p>
      </section>

      {/* MISSION & VISION */}
      <section style={styles.gridTwo}>
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Our Mission</h3>
          <p style={styles.text}>
            Our mission is to simplify complex data pipelines and enable
            organizations to process, analyze, and act on real-time data with
            confidence. We help teams move faster without sacrificing reliability.
          </p>
        </div>

        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Our Vision</h3>
          <p style={styles.text}>
            We envision a future where data flows seamlessly across systems,
            teams, and regions—unlocking intelligence at every layer of the
            enterprise without operational friction.
          </p>
        </div>
      </section>

      {/* WHAT WE DO */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>What We Do</h2>
        <p style={styles.sectionDesc}>
          Hesta Analytics provides a unified platform for real-time data ingestion,
          processing, analytics, and security—built for scale from day one.
        </p>

        <div style={styles.gridThree}>
          <div style={styles.feature}>
            <h4 style={styles.featureTitle}>Real-Time Processing</h4>
            <p style={styles.textSmall}>
              Ingest and process millions of events per second with low latency,
              ensuring your data is always fresh and actionable.
            </p>
          </div>

          <div style={styles.feature}>
            <h4 style={styles.featureTitle}>Advanced Analytics</h4>
            <p style={styles.textSmall}>
              Perform deep analytical queries and predictive analysis using a
              high-performance analytics engine optimized for speed.
            </p>
          </div>

          <div style={styles.feature}>
            <h4 style={styles.featureTitle}>Enterprise-Grade Security</h4>
            <p style={styles.textSmall}>
              Secure your data with end-to-end encryption, fine-grained access
              control, and compliance-ready architecture.
            </p>
          </div>
        </div>
      </section>

      {/* COMPANY STATS */}
      <section style={styles.stats}>
        <div style={styles.statBox}>
          <strong>2022</strong>
          <span>Founded</span>
        </div>
        <div style={styles.statBox}>
          <strong>$2.4B</strong>
          <span>Valuation</span>
        </div>
        <div style={styles.statBox}>
          <strong>140+</strong>
          <span>Employees</span>
        </div>
        <div style={styles.statBox}>
          <strong>12</strong>
          <span>Countries</span>
        </div>
      </section>

      {/* CTA */}
      <section style={styles.cta}>
        <h3 style={{ fontSize: 22, marginBottom: 12 }}>
          Learn more inside the platform
        </h3>
        <Link href="/dashboard" style={styles.ctaBtn}>
          Go to Dashboard →
        </Link>
      </section>
    </div>
  )
}

/* ================= INLINE STYLES ================= */

const styles = {
  page: {
    minHeight: '100vh',
    background: '#020617',
    color: '#e5e7eb',
    fontFamily: 'Inter, system-ui, sans-serif'
  },

  nav: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '14px 40px',
    borderBottom: '1px solid rgba(255,255,255,0.08)'
  },

  logo: {
    fontSize: 18,
    fontWeight: 700,
    color: '#3b82f6'
  },

  navLinks: {
    display: 'flex',
    gap: 24
  },

  link: {
    textDecoration: 'none',
    color: '#cbd5f5',
    fontSize: 15
  },

  primaryLink: {
    textDecoration: 'none',
    color: '#60a5fa',
    fontSize: 15,
    fontWeight: 600
  },

  header: {
    maxWidth: 900,
    margin: '50px auto 40px',
    textAlign: 'center'
  },

  title: {
    fontSize: 40,
    marginBottom: 14
  },

  subtitle: {
    fontSize: 18,
    color: '#94a3b8',
    lineHeight: 1.6
  },

  gridTwo: {
    maxWidth: 900,
    margin: '40px auto',
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 24
  },

  card: {
    background: '#020617',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: 12,
    padding: 24
  },

  cardTitle: {
    fontSize: 20,
    marginBottom: 10,
    color: '#60a5fa'
  },

  text: {
    fontSize: 16,
    lineHeight: 1.7,
    color: '#cbd5e1'
  },

  section: {
    maxWidth: 900,
    margin: '60px auto'
  },

  sectionTitle: {
    fontSize: 28,
    marginBottom: 10
  },

  sectionDesc: {
    fontSize: 17,
    color: '#94a3b8',
    marginBottom: 28
  },

  gridThree: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 20
  },

  feature: {
    background: '#020617',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: 12,
    padding: 22
  },

  featureTitle: {
    fontSize: 18,
    marginBottom: 8,
    color: '#e5e7eb'
  },

  textSmall: {
    fontSize: 15,
    lineHeight: 1.6,
    color: '#94a3b8'
  },

  stats: {
    maxWidth: 900,
    margin: '60px auto',
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: 20,
    textAlign: 'center'
  },

  statBox: {
    padding: 22,
    borderRadius: 12,
    background: '#020617',
    border: '1px solid rgba(255,255,255,0.08)',
    fontSize: 16
  },

  cta: {
    textAlign: 'center',
    padding: '50px 20px',
    borderTop: '1px solid rgba(255,255,255,0.08)'
  },

  ctaBtn: {
    display: 'inline-block',
    padding: '12px 26px',
    background: '#2563eb',
    color: '#ffffff',
    borderRadius: 8,
    textDecoration: 'none',
    fontSize: 16,
    fontWeight: 600
  }
}
