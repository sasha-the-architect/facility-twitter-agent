#!/usr/bin/env python3
"""
The Facility Twitter Agent - Railway Deployment Wrapper
Provides HTTP health check while running Twitter daemon in background.
"""

import os
import sys
import subprocess
import json
import signal
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading

# Configuration
PORT = int(os.environ.get("PORT", 8080))
DAEMON_PROCESS = None

class HealthHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress HTTP logging to reduce noise
        pass
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "facility-twitter-agent",
                "uptime_seconds": DAEMON_PROCESS.uptime() if DAEMON_PROCESS else 0
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

class DaemonProcess:
    def __init__(self):
        self.process = None
        self.start_time = datetime.utcnow()
    
    def start(self):
        """Start the Twitter agent daemon"""
        print("🚀 Starting Facility Twitter Agent daemon...")
        
        # Start the agent as a subprocess
        self.process = subprocess.Popen(
            [sys.executable, "facility_twitter_agent.py", "--mode", "daemon"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Log output in background thread
        def log_output():
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    print(f"[TwitterAgent] {line.rstrip()}")
            self.process.stdout.close()
        
        threading.Thread(target=log_output, daemon=True).start()
        
        # Wait a moment for startup
        import time
        time.sleep(2)
        
        print(f"✅ Daemon started (PID: {self.process.pid})")
    
    def uptime(self):
        return (datetime.utcnow() - self.start_time).total_seconds()
    
    def is_alive(self):
        return self.process and self.process.poll() is None
    
    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

def signal_handler(sig, frame):
    print("\n🛑 Received shutdown signal")
    if DAEMON_PROCESS:
        DAEMON_PROCESS.stop()
    sys.exit(0)

def main():
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the daemon
    global DAEMON_PROCESS
    DAEMON_PROCESS = DaemonProcess()
    DAEMON_PROCESS.start()
    
    # Start HTTP server for health checks
    print(f"📡 Health check server on port {PORT}")
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n🛑 Shutting down...")
        DAEMON_PROCESS.stop()
        server.shutdown()

if __name__ == "__main__":
    main()
