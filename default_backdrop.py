#!/usr/bin/env python3

"""
Quick script for tech person to return to default backdrop between scenes.
Run this when a scene ends and you want to clear the current background.
"""

import sys
from qlab_integration import QLab

def go_to_default():
    """Switch to default backdrop"""
    print("🎭 Switching to default backdrop...")
    
    qlab = QLab()
    success = qlab.go_to_default_backdrop()
    
    if success:
        print("✅ Switched to default backdrop")
    else:
        print("❌ Failed to switch to default backdrop")
    
    return success

def main():
    print("🎭 Improv AI - Default Backdrop Control")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage:")
        print("  python default_backdrop.py        # Switch to default backdrop")
        print("  python default_backdrop.py --help # Show this help")
        return
    
    # Quick switch to default
    go_to_default()

if __name__ == "__main__":
    main()