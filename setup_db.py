#!/usr/bin/env python3
"""
setup_db.py (Root wrapper)
Delegates execution to sql/setup_db.py
"""
import sys
import os

# Add sql directory to path and run setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql'))
from setup_db import setup_database

if __name__ == "__main__":
    setup_database()
