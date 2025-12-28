# Addy Wealth (formerly SoloWealth)

Addy Wealth is a comprehensive financial management ecosystem designed for privacy and control. It consists of a secure Desktop Application and a marketing portal.

## 🌍 Official Website
Visit **[addywealth.vercel.app](https://addywealth.vercel.app/)** to download the latest version or learn more.

![Addy Wealth Preview](website_preview.png)

---

## 🚀 Key Features
*   **🔒 100% Local Data**: Your financial data never leaves your device. Everything is stored in a secure local SQLite database.
*   **⚡ Zero Latency**: Experience native performance with no API limits or network delays.
*   **🚀 Portable**: No complicated installation required. The app is fully portable – you can even run it from a USB drive.

---

## �️ Developer Guide

### Desktop Application (Root Directory)
The core application built with Python and Electron.

**Setup & Build:**
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node modules
npm install

# 3. Build the executables
python build_desktop.py
```
*Artifacts will be in `dist/` and `electron-dist/`.*

### Marketing Website (`/website`)
The Next.js portal source code.

**Setup & Run:**
```bash
cd website
npm install
npm run dev
```

---

Addy Wealth
