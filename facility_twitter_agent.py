#!/usr/bin/env python3
"""
The Facility - Twitter/X Automation System for Railway
Autonomous engagement, reposting, and content scheduling.

Usage:
    python3 facility_twitter_agent.py --mode engage       # Engagement loop
    python3 facility_twitter_agent.py --mode post         # Post scheduled content
    python3 facility_twitter_agent.py --mode repost       # Repost relevant content
    python3 facility_twitter_agent.py --mode full         # Full automation (all modes)
    python3 facility_twitter_agent.py --mode daemon       # Run as daemon (24/7)
"""

import os
import sys
import time
import json
import random
import argparse
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

# ============================================
# CONFIGURATION
# ============================================

CONFIG = {
    # Paths
    "workspace": os.environ.get("WORKSPACE_PATH", "/workspace"),
    "tweets_dir": os.environ.get("TWEETS_DIR", "/workspace/CONTENT/tweets"),
    "config_dir": os.environ.get("CONFIG_DIR", "/workspace/config"),
    "state_file": os.environ.get("STATE_FILE", "/workspace/.facility_twitter_state.json"),
    "log_file": os.environ.get("LOG_FILE", "/workspace/logs/facility_twitter.log"),
    
    # Twitter credentials (env vars)
    "api_key": os.environ.get("TWITTER_API_KEY", ""),
    "api_secret": os.environ.get("TWITTER_API_SECRET", ""),
    "bearer_token": os.environ.get("TWITTER_BEARER_TOKEN", ""),
    "access_token": os.environ.get("TWITTER_ACCESS_TOKEN", ""),
    "access_secret": os.environ.get("TWITTER_ACCESS_SECRET", ""),
    "auth_token": os.environ.get("TWITTER_AUTH_TOKEN", ""),
    "ct0": os.environ.get("TWITTER_CT0", ""),
    
    # Rate limiting (from SUSTAINABLE_ENGAGEMENT.md)
    "rate_limit_min": int(os.environ.get("RATE_LIMIT_MIN", "60")),
    "rate_limit_max": int(os.environ.get("RATE_LIMIT_MAX", "90")),
    "daily_action_limit": int(os.environ.get("DAILY_LIMIT", "50")),
    
    # Posting schedule
    "post_times": json.loads(os.environ.get("POST_TIMES", '["08:00", "12:00", "18:00", "21:00"]')),
    
    # Reposting settings
    "repost_enabled": os.environ.get("REPOST_ENABLED", "true").lower() == "true",
    "repost_interval_hours": int(os.environ.get("REPOST_INTERVAL_HOURS", "6")),
    
    # The Facility Core Principles
    "core_principles": [
        "artist protection",
        "creative finance",
        "decentralized distribution",
        "on-chain transparency",
        "artist ownership",
        "community ownership",
        "fair treatment creators",
        "smart contracts creative"
    ],
    
    # Search queries aligned with Facility mission
    "search_queries": [
        "independent film funding",
        "creative economy web3",
        "artist ownership blockchain",
        "decentralized finance culture",
        "film crowdfunding transparency",
        "content creator investment",
        "musician funding independent",
        "writer publishing alternative",
        "smart contracts creative",
        "artist rights protection"
    ],
    
    # Accounts aligned with mission (will be expanded)
    "target_accounts": {
        "creative_economy": ["kickstarter", "indiegogo", "patreon", "substack"],
        "web3_culture": ["bankless", "messari", "glassnode", "dovey_wan"],
        "artist_advocates": ["liberalartist", "artmoneydao", "creativechain"],
        "filmmakers": ["filmindependent", "sundanceorg", "independentlens"],
        "defi_creative": ["audius", "livepeer", "rarible"]
    },
    
    # Content templates for original posts
    "content_templates": {
        "principle_intro": "The creative industry has a problem: artists can't fund projects, investors have no transparency, and gatekeepers control everything. We're building The Facility to fix it. 🧵",
        "transparency": "Here's what transparent creative finance looks like: every dollar tracked on-chain, every milestone verified, every payout automatic. No more 'where's my money?'",
        "community": "What if investors became advocates? When you own a piece of the outcome, you're not just watching—you're rooting for success.",
        "protection": "The Facility advocates for underserved artists. Our moderation layer ensures fair treatment between creators and community. Fairness isn't optional—it's the foundation."
    }
}

# ============================================
# LOGGING SETUP
# ============================================

os.makedirs(os.path.dirname(CONFIG["log_file"]), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG["log_file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# BIRD CLI WRAPPER
# ============================================

class BirdClient:
    """Wrapper for bird CLI operations"""
    
    def __init__(self, auth_token: str = "", ct0: str = ""):
        self.auth_token = auth_token or CONFIG["auth_token"]
        self.ct0 = ct0 or CONFIG["ct0"]
    
    def _build_cmd(self, base_cmd: List[str]) -> List[str]:
        """Build command with auth if available"""
        cmd = list(base_cmd)
        if self.auth_token:
            cmd.extend(["--auth-token", self.auth_token])
        if self.ct0:
            cmd.extend(["--ct0", self.ct0])
        return cmd
    
    def _run(self, cmd: List[str]) -> tuple:
        """Execute bird command and return (success, output)"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            logger.error(f"Bird command failed: {e}")
            return False, "", str(e)
    
    def tweet(self, text: str, media: Optional[str] = None) -> dict:
        """Post a tweet"""
        cmd = ["bird", "tweet", text]
        if media:
            cmd.extend(["--media", media])
        
        success, stdout, stderr = self._run(cmd)
        if success:
            logger.info(f"✅ Tweet posted: {text[:50]}...")
            return {"status": "success", "action": "tweet", "content": text[:50]}
        else:
            logger.error(f"❌ Tweet failed: {stderr}")
            return {"status": "error", "action": "tweet", "error": stderr}
    
    def retweet(self, tweet_url: str) -> dict:
        """Retweet a tweet"""
        cmd = self._build_cmd(["bird", "retweet", tweet_url])
        success, stdout, stderr = self._run(cmd)
        if success:
            logger.info(f"✅ Retweeted: {tweet_url}")
            return {"status": "success", "action": "retweet", "url": tweet_url}
        else:
            logger.error(f"❌ Retweet failed: {stderr}")
            return {"status": "error", "action": "retweet", "error": stderr}
    
    def like(self, tweet_url: str) -> dict:
        """Like a tweet"""
        cmd = self._build_cmd(["bird", "like", tweet_url])
        success, stdout, stderr = self._run(cmd)
        if success:
            logger.info(f"❤️ Liked: {tweet_url}")
            return {"status": "success", "action": "like", "url": tweet_url}
        else:
            logger.error(f"❌ Like failed: {stderr}")
            return {"status": "error", "action": "like", "error": stderr}
    
    def follow(self, username: str) -> dict:
        """Follow a user"""
        cmd = self._build_cmd(["bird", "follow", username])
        success, stdout, stderr = self._run(cmd)
        if success:
            logger.info(f"👥 Followed: @{username}")
            return {"status": "success", "action": "follow", "username": username}
        else:
            logger.error(f"❌ Follow failed: {stderr}")
            return {"status": "error", "action": "follow", "error": stderr}
    
    def reply(self, tweet_url: str, text: str) -> dict:
        """Reply to a tweet"""
        cmd = self._build_cmd(["bird", "reply", tweet_url, text])
        success, stdout, stderr = self._run(cmd)
        if success:
            logger.info(f"💬 Replied to: {tweet_url}")
            return {"status": "success", "action": "reply", "url": tweet_url}
        else:
            logger.error(f"❌ Reply failed: {stderr}")
            return {"status": "error", "action": "reply", "error": stderr}
    
    def search(self, query: str, limit: int = 10) -> dict:
        """Search tweets"""
        cmd = self._build_cmd(["bird", "search", query, "-n", str(limit)])
        success, stdout, stderr = self._run(cmd)
        if success:
            return {"status": "success", "action": "search", "query": query, "results": stdout}
        else:
            return {"status": "error", "action": "search", "error": stderr}
    
    def mentions(self, limit: int = 10) -> dict:
        """Get mentions"""
        cmd = self._build_cmd(["bird", "mentions", "-n", str(limit)])
        success, stdout, stderr = self._run(cmd)
        if success:
            return {"status": "success", "action": "mentions", "results": stdout}
        else:
            return {"status": "error", "action": "mentions", "error": stderr}
    
    def user_tweets(self, username: str, limit: int = 10) -> dict:
        """Get user's tweets"""
        cmd = self._build_cmd(["bird", "user-tweets", username, "-n", str(limit)])
        success, stdout, stderr = self._run(cmd)
        if success:
            return {"status": "success", "action": "user_tweets", "username": username, "results": stdout}
        else:
            return {"status": "error", "action": "user_tweets", "error": stderr}

# ============================================
# STATE MANAGEMENT
# ============================================

class StateManager:
    """Manage automation state"""
    
    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load state from file"""
        default_state = {
            "daily_action_count": 0,
            "last_action_date": datetime.now().date().isoformat(),
            "actions_today": [],
            "posted_tweets": [],
            "followed_accounts": [],
            "last_repost": None,
            "total_actions": 0,
            "started_at": datetime.now().isoformat()
        }
        
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return {**default_state, **json.load(f)}
            except:
                return default_state
        return default_state
    
    def save_state(self):
        """Save state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)
    
    def reset_daily_if_needed(self):
        """Reset daily counters if it's a new day"""
        today = datetime.now().date().isoformat()
        if self.state["last_action_date"] != today:
            self.state["daily_action_count"] = 0
            self.state["actions_today"] = []
            self.state["last_action_date"] = today
            self.save_state()
            logger.info("🆕 New day - daily counters reset")
    
    def can_take_action(self) -> bool:
        """Check if we can take more actions today"""
        self.reset_daily_if_needed()
        return self.state["daily_action_count"] < CONFIG["daily_action_limit"]
    
    def record_action(self, action_type: str, target: str):
        """Record an action taken"""
        self.reset_daily_if_needed()
        self.state["daily_action_count"] += 1
        self.state["total_actions"] += 1
        self.state["actions_today"].append({
            "type": action_type,
            "target": target,
            "timestamp": datetime.now().isoformat()
        })
        self.save_state()
        logger.info(f"📊 Action recorded: {action_count}/{CONFIG['daily_action_limit']} today")
    
    @property
    def action_count(self) -> int:
        return self.state["daily_action_count"]

# ============================================
# CONTENT MANAGEMENT
# ============================================

class ContentManager:
    """Manage scheduled content"""
    
    def __init__(self, tweets_dir: str):
        self.tweets_dir = tweets_dir
    
    def load_scheduled_tweets(self) -> List[dict]:
        """Load tweets marked as scheduled"""
        tweets = []
        tweets_path = Path(self.tweets_dir)
        
        if not tweets_path.exists():
            logger.warning(f"Tweets directory not found: {self.tweets_dir}")
            return tweets
        
        for file in tweets_path.glob("*.md"):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                
                # Parse frontmatter
                tweet_data = {"file": file.name}
                lines = content.split('\n')
                in_tweet = False
                tweet_lines = []
                
                for line in lines:
                    if line.startswith('---'):
                        if not in_tweet:
                            in_tweet = True
                        continue
                    if in_tweet:
                        if line.startswith('**Tweet:**'):
                            tweet_lines.append(line.replace('**Tweet:**', '').strip())
                        else:
                            tweet_lines.append(line)
                    elif ':' in line and '=' not in line:
                        key, value = line.split(':', 1)
                        tweet_data[key.strip()] = value.strip()
                
                tweet_data['content'] = '\n'.join(tweet_lines).strip()
                
                if tweet_data.get('status') in ['scheduled', 'draft']:
                    tweets.append(tweet_data)
                    
            except Exception as e:
                logger.error(f"Error parsing {file}: {e}")
        
        return tweets
    
    def get_content_for_principle(self, principle: str) -> Optional[str]:
        """Get content template for a principle"""
        templates = CONFIG.get("content_templates", {})
        return templates.get(principle)
    
    def generate_spontaneous_tweet(self) -> str:
        """Generate a spontaneous tweet aligned with Facility principles"""
        templates = list(CONFIG["content_templates"].values())
        template = random.choice(templates)
        return template

# ============================================
# ENGAGEMENT ENGINE
# ============================================

class EngagementEngine:
    """Core engagement logic"""
    
    def __init__(self, bird: BirdClient, state: StateManager):
        self.bird = bird
        self.state = state
        self.content = ContentManager(CONFIG["tweets_dir"])
    
    def _rate_limit_wait(self):
        """Wait for rate limit"""
        delay = random.randint(CONFIG["rate_limit_min"], CONFIG["rate_limit_max"])
        logger.debug(f"⏳ Rate limiting: {delay}s")
        time.sleep(delay)
    
    def _should_engage_with(self, tweet_text: str) -> bool:
        """Determine if a tweet aligns with Facility principles"""
        text_lower = tweet_text.lower()
        principles = CONFIG["core_principles"]
        
        # Check if tweet mentions any core principle keywords
        for principle in principles:
            if principle.lower() in text_lower:
                return True
        
        # Check for negative signals
        negative_keywords = ["scam", "rug", "ponzi", "fake"]
        if any(kw in text_lower for kw in negative_keywords):
            return False
        
        return False  # Default to not engaging unless clear match
    
    def run_engagement_loop(self, actions: int = 10):
        """Run engagement loop - like, follow, search"""
        logger.info(f"🚀 Starting engagement loop ({actions} actions)")
        
        for i in range(actions):
            if not self.state.can_take_action():
                logger.warning("🚫 Daily limit reached")
                break
            
            action_type = random.choice(['like', 'follow', 'search'])
            
            if action_type == 'like':
                # Search and like relevant content
                query = random.choice(CONFIG["search_queries"])
                result = self.bird.search(query, limit=5)
                if result["status"] == "success":
                    # Would parse results and like relevant ones
                    logger.info(f"🔍 Searched: {query}")
                    self.state.record_action("search", query)
            
            elif action_type == 'follow':
                # Follow aligned account
                category = random.choice(list(CONFIG["target_accounts"].keys()))
                accounts = CONFIG["target_accounts"][category]
                account = random.choice(accounts)
                result = self.bird.follow(account)
                if result["status"] == "success":
                    self.state.record_action("follow", account)
            
            elif action_type == 'search':
                # Just search and discover
                query = random.choice(CONFIG["search_queries"])
                result = self.bird.search(query, limit=10)
                if result["status"] == "success":
                    logger.info(f"🔎 Explored: {query}")
                    self.state.record_action("search", query)
            
            self._rate_limit_wait()
        
        logger.info(f"✅ Engagement loop complete: {self.state.action_count}/{CONFIG['daily_action_limit']} today")
    
    def run_repost_loop(self, max_reposts: int = 5):
        """Find and repost relevant content"""
        if not CONFIG["repost_enabled"]:
            logger.info("Reposting disabled in config")
            return
        
        logger.info(f"🔄 Starting repost loop ({max_reposts} reposts)")
        
        for i in range(max_reposts):
            if not self.state.can_take_action():
                break
            
            query = random.choice(CONFIG["search_queries"])
            result = self.bird.search(query, limit=10)
            
            if result["status"] == "success":
                # Would parse and find best tweet to repost
                # For now, just log
                logger.info(f"📰 Found content for: {query}")
                self.state.record_action("repost_search", query)
            
            self._rate_limit_wait()
        
        logger.info("✅ Repost loop complete")
    
    def run_posting_loop(self):
        """Post scheduled content"""
        logger.info("📝 Starting posting loop")
        
        tweets = self.content.load_scheduled_tweets()
        
        for tweet in tweets:
            if not self.state.can_take_action():
                break
            
            result = self.bird.tweet(tweet['content'])
            if result["status"] == "success":
                self.state.record_action("post", tweet['file'])
                # Update tweet status in file
                self._mark_tweet_posted(tweet['file'])
            
            self._rate_limit_wait()
        
        logger.info("✅ Posting loop complete")
    
    def _mark_tweet_posted(self, filename: str):
        """Mark a tweet file as posted"""
        filepath = os.path.join(CONFIG["tweets_dir"], filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            
            content = content.replace('status: scheduled', 'status: posted')
            content = content.replace('status: draft', 'status: posted')
            
            with open(filepath, 'w') as f:
                f.write(content)
    
    def run_full_cycle(self):
        """Run complete automation cycle"""
        logger.info("🎯 Starting full automation cycle")
        
        # Post scheduled content
        self.run_posting_loop()
        
        # Engagement loop
        remaining = CONFIG["daily_action_limit"] - self.state.action_count
        if remaining > 5:
            self.run_engagement_loop(min(remaining - 5, 15))
        
        # Repost loop (if enabled)
        if CONFIG["repost_enabled"]:
            remaining = CONFIG["daily_action_limit"] - self.state.action_count
            if remaining > 3:
                self.run_repost_loop(min(remaining - 3, 5))
        
        logger.info(f"🏁 Full cycle complete - {self.state.action_count}/{CONFIG['daily_action_limit']} today")

# ============================================
# DAEMON MODE
# ============================================

class Daemon:
    """Run automation as a persistent daemon"""
    
    def __init__(self, bird: BirdClient, state: StateManager, engine: EngagementEngine):
        self.bird = bird
        self.state = state
        self.engine = engine
        self.running = True
    
    def _should_post_now(self) -> bool:
        """Check if it's time to post scheduled content"""
        now = datetime.now().strftime("%H:%M")
        return now in CONFIG["post_times"]
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("🛑 Shutdown signal received")
        self.running = False
    
    def run(self):
        """Main daemon loop"""
        import signal
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        logger.info("🚀 Facility Twitter Agent starting in daemon mode")
        logger.info(f"📊 Rate limit: {CONFIG['daily_action_limit']}/day")
        logger.info(f"⏰ Post times: {CONFIG['post_times']}")
        
        while self.running:
            try:
                # Check daily reset
                self.state.reset_daily_if_needed()
                
                # Run full cycle if within limits
                if self.state.can_take_action():
                    self.engine.run_full_cycle()
                
                # Wait between cycles
                logger.info("💤 Sleeping until next cycle...")
                time.sleep(3600)  # Check every hour
                
            except Exception as e:
                logger.error(f"Daemon error: {e}")
                time.sleep(60)  # Wait 1 min on error before retry
        
        logger.info("👋 Facility Twitter Agent stopped")

# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    parser = argparse.ArgumentParser(description="The Facility Twitter Automation")
    parser.add_argument("--mode", choices=["engage", "post", "repost", "full", "daemon"],
                        default="full", help="Operation mode")
    parser.add_argument("--actions", type=int, default=10,
                        help="Number of actions for engage mode")
    parser.add_argument("--reposts", type=int, default=5,
                        help="Number of reposts for repost mode")
    
    args = parser.parse_args()
    
    # Initialize components
    bird = BirdClient()
    state = StateManager(CONFIG["state_file"])
    engine = EngagementEngine(bird, state)
    
    logger.info(f"🏛️ Facility Twitter Agent - Mode: {args.mode}")
    
    if args.mode == "engage":
        engine.run_engagement_loop(args.actions)
    elif args.mode == "post":
        engine.run_posting_loop()
    elif args.mode == "repost":
        engine.run_repost_loop(args.reposts)
    elif args.mode == "full":
        engine.run_full_cycle()
    elif args.mode == "daemon":
        daemon = Daemon(bird, state, engine)
        daemon.run()
    
    logger.info("✅ Facility Twitter Agent finished")

if __name__ == "__main__":
    main()
