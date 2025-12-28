import Link from 'next/link';

export default function Home() {
  return (
    <main>
      {/* Navigation */}
      <nav className="navbar">
        <div className="logo">
          <span className="logo-icon">AW</span>
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
            <a href="/releases/AddyWealth-App.exe" download className="btn-primary">
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
                <div className="mock-card balance">
                  <h3>Total Net Worth</h3>
                  <div className="val">$124,592.00</div>
                </div>
                <div className="mock-card"></div>
                <div className="mock-card"></div>
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
            <p>Built for privacy enthusiasts who want powerful tracking without the cloud risk.</p>
          </div>

          <div className="feature-grid">
            <div className="feature-card">
              <div className="icon-box">🔒</div>
              <h3>100% Local Data</h3>
              <p>Your financial data never leaves the device. It lives in a secure SQLite database on your machine.</p>
            </div>
            <div className="feature-card">
              <div className="icon-box">⚡</div>
              <h3>Zero Latency</h3>
              <p>Native performance. No loading spinners, no API limits. Just instant access to your numbers.</p>
            </div>
            <div className="feature-card">
              <div className="icon-box">🚀</div>
              <h3>Portable App</h3>
              <p>No installation required. Carry the app and your database on a USB drive if you want.</p>
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
