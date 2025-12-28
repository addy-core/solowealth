import Link from 'next/link';

export default function Home() {
  return (
    <main>
      {/* Navigation */}
      <nav className="navbar">
        <div className="logo">
          {/* Logo SVG */}
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L2 28H30L16 2Z" fill="url(#logo_gradient)" stroke="var(--accent-primary)" strokeWidth="2" />
            <path d="M16 8L8 24H24L16 8Z" fill="var(--bg-color)" />
            <defs>
              <linearGradient id="logo_gradient" x1="16" y1="2" x2="16" y2="28" gradientUnits="userSpaceOnUse">
                <stop stopColor="var(--accent-primary)" />
                <stop offset="1" stopColor="#0f172a" />
              </linearGradient>
            </defs>
          </svg>
          <span className="logo-text">Addy Wealth</span>
        </div>
        <div className="nav-links">
          <Link href="#features">Features</Link>
          <Link href="#privacy">Privacy</Link>
          <Link href="#" className="btn-primary small">Download</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="hero">
        <div className="hero-content">
          <span className="badge">v1.0 Release Now Available</span>
          <h1>
            Your Wealth.<br />
            <span className="text-gradient">Your Control.</span>
          </h1>
          <p className="hero-sub">
            The secure, local-first personal finance tracker.
            Manage your portfolio without sharing data with the cloud.
            Zero logins. Zero monthly fees.
          </p>

          <div className="btn-group">
            <a href={process.env.NEXT_PUBLIC_DOWNLOAD_URL || '#'} className="btn-primary">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
              </svg>
              Download for Windows
            </a>
            <Link href="#features" className="btn-secondary">
              Learn More
            </Link>
          </div>

          <div className="download-info">
            <span>Windows 10/11</span> • <span>Portable .Exe</span> • <span>Free & Open</span>
          </div>
        </div>

        {/* App Preview */}
        <div className="hero-visual">
          <div className="app-window">
            <div className="window-header">
              <div className="dots"><span></span><span></span><span></span></div>
              <div className="address-bar">addy-wealth://dashboard</div>
            </div>
            <div className="window-content">
              {/* Abstract Dashboard Mockup */}
              <div className="mock-grid">
                {/* Balance Card */}
                <div className="mock-card balance">
                  <h3>Total Net Worth</h3>
                  <div className="val">$124,592.00</div>
                  {/* Mini trend line */}
                  <svg width="100%" height="40" viewBox="0 0 200 40" style={{ marginTop: 'auto', opacity: 0.5 }}>
                    <path d="M0 35 C50 35, 50 10, 100 20 C150 30, 150 5, 200 15" fill="none" stroke="var(--accent-primary)" strokeWidth="2" />
                  </svg>
                </div>

                {/* Abstract Chart Card */}
                <div className="mock-card" style={{ display: 'flex', alignItems: 'flex-end', padding: '20px', gap: '8px' }}>
                  <div style={{ width: '20%', height: '40%', background: 'var(--accent-primary)', opacity: 0.3, borderRadius: '4px' }}></div>
                  <div style={{ width: '20%', height: '70%', background: 'var(--accent-primary)', opacity: 0.6, borderRadius: '4px' }}></div>
                  <div style={{ width: '20%', height: '50%', background: 'var(--accent-primary)', opacity: 0.4, borderRadius: '4px' }}></div>
                  <div style={{ width: '20%', height: '90%', background: 'var(--accent-primary)', opacity: 0.9, borderRadius: '4px' }}></div>
                </div>

                {/* Pie Chart Card - Visual */}
                <div className="mock-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <svg width="80" height="80" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.1)" strokeWidth="10" fill="none" />
                    <circle cx="50" cy="50" r="40" stroke="var(--accent-primary)" strokeWidth="10" fill="none" strokeDasharray="180 250" transform="rotate(-90 50 50)" strokeLinecap="round" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section id="features" className="features">
        <div className="container">
          <div className="section-header">
            <h2>Why Choose Addy Wealth?</h2>
            <p style={{ color: 'var(--text-secondary)' }}>Built for privacy enthusiasts who want powerful tracking without the cloud risk.</p>
          </div>

          <div className="feature-grid">
            <div className="feature-card">
              <div className="icon-box">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <h3>100% Local Data</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Your financial data never leaves the device. It lives in a secure SQLite database on your machine.</p>
            </div>
            <div className="feature-card">
              <div className="icon-box">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
              </div>
              <h3>Zero Latency</h3>
              <p style={{ color: 'var(--text-secondary)' }}>Native performance. No loading spinners, no API limits. Just instant access to your numbers.</p>
            </div>
            <div className="feature-card">
              <div className="icon-box">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
                  <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
                  <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path>
                  <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path>
                </svg>
              </div>
              <h3>Portable App</h3>
              <p style={{ color: 'var(--text-secondary)' }}>No installation required. Carry the app and your database on a USB drive if you want.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer>
        <div className="footer-content">
          <p>&copy; 2025 Addy Wealth. Built with Electron + Python.</p>
        </div>
      </footer>
    </main>
  );
}
