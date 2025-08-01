#!/usr/bin/env python3

"""
Tech Control Panel for Improv AI Background Generator
Quick controls for tech person during live shows
"""

import sys
import os
from qlab_integration import QLab

def show_menu():
    """Show the tech control menu"""
    print("\n🎭 IMPROV AI - TECH CONTROL PANEL")
    print("=" * 40)
    print("1. Go to default backdrop")
    print("2. Stop current background") 
    print("3. Show current status")
    print("4. Exit")
    print("-" * 40)

def tech_control():
    """Main tech control interface"""
    qlab = QLab()
    
    while True:
        show_menu()
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            print("\n🎭 Switching to default backdrop...")
            success = qlab.go_to_default_backdrop()
            if success:
                print("✅ Switched to default backdrop")
            else:
                print("❌ Failed to switch to default backdrop")
        
        elif choice == "2":
            print("\n🛑 Stopping current background...")
            if qlab.last_cue_id:
                success = qlab.go_to_default_backdrop()  # This stops current and goes to default
                if success:
                    print("✅ Stopped current background")
                else:
                    print("❌ Failed to stop background")
            else:
                print("ℹ️  No active background to stop")
        
        elif choice == "3":
            print(f"\n📊 STATUS:")
            print(f"   Last cue ID: {qlab.last_cue_id or 'None'}")
            print(f"   Default backdrop ID: {qlab.default_backdrop_id or 'Not created'}")
            print(f"   Auto-stop enabled: {qlab.auto_stop_previous}")
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

def quick_default():
    """Quick default backdrop switch (no menu)"""
    qlab = QLab()
    print("🎭 Quick switch to default backdrop...")
    success = qlab.go_to_default_backdrop()
    if success:
        print("✅ Switched to default backdrop")
    else:
        print("❌ Failed to switch to default backdrop")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "default" or sys.argv[1] == "d":
            quick_default()
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("🎭 Improv AI Tech Control")
            print("\nUsage:")
            print("  python tech_control.py           # Interactive menu")
            print("  python tech_control.py default   # Quick default backdrop")
            print("  python tech_control.py d         # Quick default backdrop (short)")
            print("  python tech_control.py --help    # Show this help")
            return
    
    # Run interactive menu
    tech_control()

if __name__ == "__main__":
    main()