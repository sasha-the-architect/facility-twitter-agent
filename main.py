#!/usr/bin/env python3
"""
The Facility Twitter Agent - Main Entry Point
Wraps facility_twitter_agent.py for Railway/Railpack auto-detection
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main function
from facility_twitter_agent import main

if __name__ == "__main__":
    main()
