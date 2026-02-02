# The Facility - Railway Twitter Automation

Deploy autonomous Twitter/X engagement to Railway for 24/7 operation.

## 🚀 Quick Deploy

### 1. Prepare Your Repository

```bash
cd /workspace/projects/the-facility
git add .
git commit -m "Add Railway Twitter automation"
git push origin main
```

### 2. Deploy to Railway

**Option A: CLI**
```bash
railway login
railway init
railway up
```

**Option B: Web**
1. Go to https://railway.app
2. Connect your GitHub repo
3. Select the project
4. Configure environment variables (see below)
5. Deploy

### 3. Configure Environment Variables

In Railway dashboard, set these variables:

| Variable | Value | Required |
|----------|-------|----------|
| `TWITTER_AUTH_TOKEN` | Your Twitter auth_token cookie | ✅ Yes |
| `TWITTER_CT0` | Your Twitter ct0 cookie | ✅ Yes |
| `RATE_LIMIT_MIN` | `60` | No |
| `RATE_LIMIT_MAX` | `90` | No |
| `DAILY_LIMIT` | `50` | No |
| `REPOST_ENABLED` | `true` | No |

**Getting Twitter Cookies:**
1. Open x.com in browser (Chrome/Arc)
2. Open DevTools (Cmd+Option+I)
3. Go to Application → Cookies → https://x.com
4. Copy `auth_token` and `ct0` values
5. Add to Railway environment variables

### 4. Sync Content (Optional)

For scheduled tweets, mount a volume or sync from your main workspace:

```bash
# Sync tweets to Railway
railway run cp -r /workspace/CONTENT/tweets ./CONTENT/
```

Or configure a Git sync for the `CONTENT/` folder.

## 📁 Project Structure

```
the-facility/
├── facility_twitter_agent.py   # Main automation script
├── railway.json                # Railway configuration
├── README.md                   # This file
├── CONTENT/
│   └── tweets/                 # Scheduled tweet drafts
│       ├── tweet_01.md
│       ├── tweet_02.md
│       └── tweet_03.md
└── config/
    └── (config files)
```

## 🎛️ Operation Modes

### Daemon Mode (Default - 24/7)
```bash
python3 facility_twitter_agent.py --mode daemon
```
- Runs continuously
- Checks every hour for actions
- Posts at scheduled times
- Respects daily limits

### Full Cycle (Daily Run)
```bash
python3 facility_twitter_agent.py --mode full
```
- Posts scheduled content
- Runs engagement loop
- Runs repost loop
- One-shot execution

### Engagement Only
```bash
python3 facility_twitter_agent.py --mode engage --actions 15
```
- Likes, follows, searches
- Custom action count

### Posting Only
```bash
python3 facility_twitter_agent.py --mode post
```
- Posts scheduled tweets
- No engagement

### Reposting Only
```bash
python3 facility_twitter_agent.py --mode repost --reposts 5
```
- Finds and reposts relevant content
- Custom repost count

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKSPACE_PATH` | `/workspace` | Base workspace directory |
| `TWEETS_DIR` | `/workspace/CONTENT/tweets` | Scheduled tweets location |
| `CONFIG_DIR` | `/workspace/config` | Configuration directory |
| `STATE_FILE` | `/workspace/.facility_twitter_state.json` | State tracking file |
| `LOG_FILE` | `/workspace/logs/facility_twitter.log` | Log file path |
| `TWITTER_AUTH_TOKEN` | - | Twitter cookie (required) |
| `TWITTER_CT0` | - | Twitter cookie (required) |
| `RATE_LIMIT_MIN` | `60` | Min seconds between actions |
| `RATE_LIMIT_MAX` | `90` | Max seconds between actions |
| `DAILY_LIMIT` | `50` | Max actions per day |
| `REPOST_ENABLED` | `true` | Enable auto-reposting |
| `REPOST_INTERVAL_HOURS` | `6` | Hours between repost cycles |
| `POST_TIMES` | `["08:00", "12:00", "18:00", "21:00"]` | Posting schedule (PST) |

### Customizing Content

Add new tweets to `CONTENT/tweets/`:

```markdown
---
date: 2026-02-02
status: scheduled
platform: twitter
business: The Facility
type: principle
---

**Tweet:**

Your tweet content here...

#Hashtags
```

### Adding Target Accounts

Edit `facility_twitter_agent.py` and update `CONFIG["target_accounts"]`:

```python
"target_accounts": {
    "creative_economy": ["account1", "account2", ...],
    "web3_culture": ["account3", "account4", ...],
    # Add more categories
}
```

## 📊 Monitoring

### Check Logs
```bash
railway logs -t
```

### Check State
```bash
railway run cat .facility_twitter_state.json
```

### Health Check
The agent logs "🏁 Full cycle complete" after each cycle.

## 🛡️ Safety Features

1. **Rate Limiting**: 1 action per 60-90 seconds
2. **Daily Caps**: Max 50 actions per day
3. **Smart Scheduling**: Spread actions throughout day
4. **State Persistence**: Resume from saved state
5. **Graceful Shutdown**: Handles SIGTERM/SIGINT

## 🔧 Troubleshooting

### "Bird command not found"
Install bird CLI in Dockerfile or use nixpacks:
```dockerfile
RUN npm install -g @steipete/bird
```

### Rate Limited
- Wait for limit to reset (usually 15 min - 2 hours)
- Reduce `DAILY_LIMIT` if persistent

### Authentication Failed
- Refresh Twitter cookies
- Ensure both `auth_token` and `ct0` are set

### No Tweets Found
- Check `TWEETS_DIR` path
- Verify tweets have `status: scheduled`

## 📈 Expected Performance

| Metric | Daily | Weekly | Monthly |
|--------|-------|--------|---------|
| Followers | +5-10 | +35-70 | +150-300 |
| Engagement Actions | 45-50 | 315-350 | 1,350-1,500 |
| Content Posts | 2-3 | 14-21 | 60-90 |

## 🚦 Deployment Checklist

- [ ] Twitter account created (@TheFacilityXYZ)
- [ ] Profile configured (bio, avatar, banner)
- [ ] Cookies extracted and set as env vars
- [ ] Tweet drafts created in CONTENT/tweets/
- [ ] Test run completed locally
- [ ] Deployed to Railway
- [ ] Logs confirming successful operation
- [ ] Monitoring set up (optional)

## 📚 Related Documentation

- [Twitter Automation Guide](./TWITTER_AUTOMATION.md)
- [Sustainable Engagement Strategy](./SUSTAINABLE_ENGAGEMENT.md)
- [Core Operating Principles](../../AGENTS.md)

---

*Built for The Facility - The future of creative finance*
