"""
config.py - Central path configuration for the project.
All scripts import paths from here instead of computing from __file__.
"""

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
PLOTS_DIR = os.path.join(OUTPUT_DIR, 'plots')
