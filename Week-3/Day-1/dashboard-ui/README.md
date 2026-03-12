# Dashboard UI — Day 1

## Tech Stack
- Next.js (App Router)
- React
- Tailwind CSS
- PostCSS

## What Was Built
- Header (Navbar)
  - Project title: Hesta Analytics
  - Search input
  - User icon
- Sidebar
  - Dashboard
  - Pages
  - Charts
  - Tables
- Dashboard content placeholder

## Folder Structure
```
app/
 ├─ layout.js      // Global layout (Navbar + Sidebar)
 ├─ page.js        // Dashboard page
 └─ globals.css    // Tailwind base styles

components/
 └─ ui/
    ├─ Navbar.jsx
    └─ Sidebar.jsx
```
## Screenshot
![Dashboard UI](./dashboard.png)

## Key Learnings
- App Router is file-structure driven
- layout.js wraps all pages automatically
- page.js represents a route
- Tailwind generates CSS at build time based on scanned paths
- Wrong paths or config can remove styling without runtime errors
- UI issues are often configuration issues, not CSS issues



First, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

