#!/usr/bin/env python3

import subprocess
import os

def test_working_qlab():
    """Test the simplest working QLab approach"""
    
    image_path = "/Users/timothylebon/dev/improv-ai/generated_images/background_1752916052.png"
    
    if not os.path.exists(image_path):
        print("Image doesn't exist")
        return
    
    print("Testing simple QLab integration...")
    
    # Test 1: Create cue
    create_script = '''
tell application "QLab"
    tell front workspace
        make type "Video"
    end tell
end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', create_script], capture_output=True, text=True, timeout=10)
        print(f"Create result: {result.returncode}, {result.stderr}")
    except Exception as e:
        print(f"Create error: {e}")
        return
    
    # Test 2: Get last cue and set file
    set_script = f'''
tell application "QLab"
    tell front workspace
        set lastCue to last item of cues
        set file target of lastCue to "{image_path}"
        set q name of lastCue to "AI Test"
        start lastCue
    end tell
end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', set_script], capture_output=True, text=True, timeout=10)
        print(f"Set result: {result.returncode}, {result.stderr}")
        if result.returncode == 0:
            print("✅ Success!")
        else:
            print(f"❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"Set error: {e}")

if __name__ == "__main__":
    test_working_qlab()