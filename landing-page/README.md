# The Facility - Landing Page

A modern, responsive landing page for The Facility creative finance platform.

## Quick Deploy Options

### Option 1: Vercel (Recommended)
```bash
cd landing-page
npx vercel
```

### Option 2: Netlify
```bash
cd landing-page
npx netlify deploy --prod
```

### Option 3: Cloudflare Pages
```bash
cd landing-page
npx wrangler pages deploy
```

### Option 4: GitHub Pages
1. Push `landing-page/` folder to a GitHub repo
2. Go to Settings > Pages > Enable from main branch
3. Custom domain: `thefacility.xyz`

## Local Development
```bash
cd landing-page
python3 -m http.server 8080
# Open http://localhost:8080
```

## Files
- `index.html` - Main landing page
- `favicon.png` - Brand favicon

## Features
- Fully responsive design
- Dark mode optimized
- Smooth animations
- Email signup form (form handling to be connected)
- Social links (X/Twitter, Discord, Email)
- Open Graph meta tags for social sharing

## To Do
- [ ] Connect email form to database (Supabase, Airtable, or email service)
- [ ] Replace placeholder links with real URLs
- [ ] Add analytics (Vercel Analytics, Google Analytics, etc.)
- [ ] Custom domain configuration
- [ ] OG image generation
