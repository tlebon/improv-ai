#!/usr/bin/env python3

import subprocess
import os

def test_simple_qlab():
    """Test simplified QLab integration"""
    print("🎬 Testing Simple QLab Integration")
    print("=" * 35)
    
    # Test 1: Basic communication
    print("1. Testing basic QLab communication...")
    try:
        script = '''
        tell application "QLab 5"
            return "QLab is responding"
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        print(f"   Response: '{result.stdout.strip()}'")
        if result.returncode == 0:
            print("   ✅ QLab responding")
        else:
            print(f"   ❌ Error: {result.stderr}")
            return
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return
    
    # Test 2: Create a memo cue (simpler than video)
    print("\n2. Testing memo cue creation...")
    try:
        script = '''
        tell application "QLab 5"
            tell front document
                set newCue to make type "Memo"
                set q name of newCue to "Test Memo"
                return "Created: " & q name of newCue
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        print(f"   Response: '{result.stdout.strip()}'")
        if result.returncode == 0:
            print("   ✅ Memo cue created successfully")
        else:
            print(f"   ❌ Error: {result.stderr}")
            return
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return
    
    # Test 3: Try to create video cue with a test image
    print("\n3. Testing video cue creation...")
    
    # Create a dummy text file to test with (since we don't have an actual image)
    test_file = "/tmp/test_image.txt"
    with open(test_file, 'w') as f:
        f.write("test")
    
    try:
        script = f'''
        tell application "QLab 5"
            tell front document
                set newCue to make type "Video"
                set file target of newCue to "{test_file}"
                set q name of newCue to "Test Video"
                return "Created video cue"
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        print(f"   Response: '{result.stdout.strip()}'")
        if result.returncode == 0:
            print("   ✅ Video cue syntax works")
        else:
            print(f"   ❌ Error: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_simple_qlab()