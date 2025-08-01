#!/usr/bin/env python3

import subprocess

def test_qlab_detection():
    """Test QLab detection methods"""
    print("🎬 Testing QLab Detection")
    print("=" * 30)
    
    # Test 1: Check running processes
    print("1. Checking running processes...")
    try:
        check_script = '''
        tell application "System Events"
            return (name of processes) contains "QLab 5"
        end tell
        '''
        result = subprocess.run(['osascript', '-e', check_script], capture_output=True, text=True, timeout=5)
        print(f"   Return code: {result.returncode}")
        print(f"   Output: '{result.stdout.strip()}'")
        print(f"   Error: '{result.stderr.strip()}'")
        
        if "true" in result.stdout.lower():
            print("   ✅ QLab 5 detected in processes")
        else:
            print("   ❌ QLab 5 not detected in processes")
    except Exception as e:
        print(f"   ❌ Error checking processes: {e}")
    
    # Test 2: Try to communicate with QLab directly
    print("\n2. Testing direct QLab communication...")
    try:
        test_script = '''
        tell application "QLab 5"
            return "QLab is responding"
        end tell
        '''
        result = subprocess.run(['osascript', '-e', test_script], capture_output=True, text=True, timeout=10)
        print(f"   Return code: {result.returncode}")
        print(f"   Output: '{result.stdout.strip()}'")
        print(f"   Error: '{result.stderr.strip()}'")
        
        if result.returncode == 0:
            print("   ✅ QLab 5 is responding")
        else:
            print("   ❌ QLab 5 not responding")
    except Exception as e:
        print(f"   ❌ Error communicating with QLab: {e}")
    
    # Test 3: Check workspace count
    print("\n3. Testing workspace detection...")
    try:
        workspace_script = '''
        tell application "QLab 5"
            return count of workspaces
        end tell
        '''
        result = subprocess.run(['osascript', '-e', workspace_script], capture_output=True, text=True, timeout=10)
        print(f"   Return code: {result.returncode}")
        print(f"   Output: '{result.stdout.strip()}'")
        print(f"   Error: '{result.stderr.strip()}'")
        
        if result.returncode == 0:
            workspace_count = result.stdout.strip()
            print(f"   ✅ Found {workspace_count} workspace(s)")
        else:
            print("   ❌ Could not get workspace count")
    except Exception as e:
        print(f"   ❌ Error checking workspaces: {e}")
    
    # Test 4: Try creating a simple cue
    print("\n4. Testing cue creation...")
    try:
        cue_script = '''
        tell application "QLab 5"
            if (count of workspaces) > 0 then
                tell front workspace
                    set testCue to make type "Memo"
                    set q name of testCue to "Test Cue"
                    return "Created test cue: " & q name of testCue
                end tell
            else
                return "No workspace available"
            end if
        end tell
        '''
        result = subprocess.run(['osascript', '-e', cue_script], capture_output=True, text=True, timeout=10)
        print(f"   Return code: {result.returncode}")
        print(f"   Output: '{result.stdout.strip()}'")
        print(f"   Error: '{result.stderr.strip()}'")
        
        if result.returncode == 0:
            print("   ✅ Successfully created test cue")
        else:
            print("   ❌ Failed to create test cue")
    except Exception as e:
        print(f"   ❌ Error creating test cue: {e}")

if __name__ == "__main__":
    test_qlab_detection()