#!/usr/bin/env python3
"""
eda_and_scorecard.py (Root wrapper)
Delegates execution to python/eda_and_scorecard.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))
from eda_and_scorecard import calculate_scorecard

if __name__ == "__main__":
    calculate_scorecard()
