#!/usr/bin/env python3

import subprocess

def test_correct_qlab_syntax():
    """Test correct QLab 5 syntax"""
    print("🎬 Testing Correct QLab 5 Syntax")
    print("=" * 32)
    
    # Test with the correct QLab 5 AppleScript syntax
    print("1. Testing workspace access...")
    try:
        script = '''
tell application "QLab 5"
    tell workspace 1
        return "Workspace accessible"
    end tell
end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        print(f"   Response: '{result.stdout.strip()}'")
        print(f"   Error: '{result.stderr.strip()}'")
        if result.returncode == 0:
            print("   ✅ Workspace access works")
        else:
            print("   ❌ Workspace access failed")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print("\n2. Testing cue creation...")
    try:
        script = '''
tell application "QLab 5"
    tell workspace 1
        set newCue to make type "Memo"
        set q name of newCue to "Test from Python"
        return q name of newCue
    end tell
end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        print(f"   Response: '{result.stdout.strip()}'")
        print(f"   Error: '{result.stderr.strip()}'")
        if result.returncode == 0:
            print("   ✅ Cue creation works")
        else:
            print("   ❌ Cue creation failed")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_correct_qlab_syntax()