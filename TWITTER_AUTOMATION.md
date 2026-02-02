# The Facility - Twitter/X Automation Guide
**Setup Complete:** February 1, 2026 - 11:35 AM PST

---

## 🔐 Authentication Status

**Account:** @TheFacilityXYZ  
**Status:** ✅ Authenticated via Chrome cookies  
**Bird Config:** `~/.config/bird/config.json5`

---

## ✅ CAPABILITIES (Working)

### Reading & Discovery
```bash
# Read tweets from any user
bird user-tweets @username -n 10

# Search tweets
bird search "creative finance" -n 10

# Read specific tweet
bird https://x.com/user/status/123456

# Get user's profile info
bird about @username

# Check trending
bird news -n 10
bird trending

# Get mentions
bird mentions -n 10
```

### Engagement
```bash
# Follow users
bird follow @crypto @web3 @defi

# Reply to tweets (copy link first)
bird reply https://x.com/user/status/123456 "Great thread!"

# Like tweets
bird like https://x.com/user/status/123456

# Quote tweets
bird quote https://x.com/user/status/123456 "My take on this..."

# Retweet
bird retweet https://x.com/user/status/123456
```

### Posting (Media Supported)
```bash
# Simple tweet
bird tweet "Hello world!"

# Tweet with image
bird tweet "Check this out!" --media path/to/image.png --alt "Description"

# Tweet with multiple images (up to 4)
bird tweet "Gallery" --media a.jpg --media b.jpg --media c.jpg

# Thread reply
bird reply <url> "First point..."

# Thread thread reply
bird reply <url> "Second point..."
```

---

## 📋 TWEET DRAFTS READY

**Location:** `/workspace/CONTENT/tweets/`

| File | Type | Status |
|------|------|--------|
| `tweet_01.md` | Introduction thread starter | ✅ Ready |
| `tweet_02.md` | Film financing wisdom | ✅ Ready |
| `tweet_03.md` | Community question | ✅ Ready |

---

## 🎨 BRAND ASSETS READY

**Location:** `/workspace/CONTENT/facility_brand/`

| Asset | File | Size | Purpose |
|-------|------|------|---------|
| Profile Pic | `profile_picture.png` | 1.4 MB | X Profile picture |
| Banner | `banner.png` | 6.6 MB | X Profile header |

**To upload:**
- Upload via browser manually, OR
- Use `bird tweet --media` when posting

---

## 🔄 CONTENT PLAN (From Reference Doc)

### 10 Topics for Engagement
From `projects/the-facility/The Facility copy.txt`:

1. **Non-crypto users** - Creative industry problems, funding struggles
2. **DeFi/DePIN** - Smart contracts for creative projects
3. **Crowdfunding** - Better than traditional models
4. **Film financing** - Transparent milestone-based funding
5. **Artist ownership** - Creators keeping control
6. **Gatekeepers** - Why traditional systems fail artists
7. **Decentralized distribution** - No middlemen
8. **Community ownership** - Investors become advocates
9. **Transparency** - Blockchain-verified everything
10. **Future of creative work** - Tokenized intellectual property

### Posting Strategy
- **Week 1:** Introduction tweets (3 drafted)
- **Week 2-4:** Educational content (10 topics)
- **Engagement:** Reply to relevant crypto/creative accounts
- **Goal:** 10K followers → Token launch → Airdrop

---

## ⚠️ RATE LIMITING NOTES

From bird skill docs:
> Posting is more likely to be rate limited; if blocked, use the browser tool instead.

**Mitigation:**
- Space out posts (1-2 hours minimum)
- Mix engagement (likes, replies) with posting
- Don't post too frequently in first week
- If blocked → wait or use browser for manual post

---

## 📊 USAGE EXAMPLES

### Daily Engagement Routine
```bash
# Morning: Check mentions
bird mentions -n 10

# Engage with relevant accounts
bird like https://x.com/crypto/status/...
bird follow @web3creator

# Search for opportunities
bird search "film funding" -n 10
bird search "creative projects" -n 10
```

### Content Creation
```bash
# Post with image
bird tweet "The future of creative finance" --media banner.png

# Reply to thread
bird reply <url> "This is exactly what we're building at The Facility..."

# Quote tweet with insight
bird quote <url> "Our take on this at The Facility 👇"
```

---

## 🔗 QUICK REFERENCE

| Action | Command |
|--------|---------|
| Post tweet | `bird tweet "..."` |
| Post with image | `bird tweet "..." --media file.png` |
| Reply | `bird reply <url> "..."` |
| Follow | `bird follow @user` |
| Like | `bird like <url>` |
| Search | `bird search "query" -n 10` |
| My tweets | `bird user-tweets @TheFacilityXYZ -n 10` |
| My mentions | `bird mentions -n 10` |
| Trending | `bird trending` |

---

## 🚀 NEXT STEPS

### For Manual Operation (Local)

1. **Run the automation script:**
```bash
python3 /workspace/projects/the-facility/facility_twitter_agent.py --mode full
```

2. **Or run engagement only:**
```bash
python3 /workspace/projects/the-facility/facility_twitter_agent.py --mode engage --actions 15
```

### For Autonomous Operation (Railway Deploy)

**See: [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)**

The Railway deployment provides:
- 24/7 autonomous operation
- Automatic restarts on failure
- Environment variable configuration
- Log persistence
- Scheduled posting at 8AM, 12PM, 6PM, 9PM PST

**Quick Deploy:**
1. Push this folder to GitHub
2. Connect repo to Railway.app
3. Set `TWITTER_AUTH_TOKEN` and `TWITTER_CT0` environment variables
4. Deploy using `railway.json` config

---

*Last Updated: Feb 1, 2026 11:20 PM PST*
*Status: Railway deployment ready*
