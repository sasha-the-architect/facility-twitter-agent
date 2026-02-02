FROM python:3.11-slim

# Install Node.js for bird CLI
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install bird CLI
RUN npm install -g @steipete/bird

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY facility_twitter_agent.py .

# Create directories
RUN mkdir -p logs CONTENT/tweets config

# Set environment variables
ENV PYTHONPATH=/app \
    WORKSPACE_PATH=/app \
    TWEETS_DIR=/app/CONTENT/tweets \
    CONFIG_DIR=/app/config \
    STATE_FILE=/app/.facility_twitter_state.json \
    LOG_FILE=/app/logs/facility_twitter.log \
    RATE_LIMIT_MIN=60 \
    RATE_LIMIT_MAX=90 \
    DAILY_LIMIT=50 \
    REPOST_ENABLED=true

# Default command
CMD ["python3", "facility_twitter_agent.py", "--mode", "daemon"]
