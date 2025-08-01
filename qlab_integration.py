import subprocess
import os
from typing import Optional

class QLab:
    def __init__(self, workspace_name: Optional[str] = None, auto_stop_previous: bool = True):
        self.workspace_name = workspace_name
        self.auto_stop_previous = auto_stop_previous
        self.last_cue_id = None
        self.default_backdrop_id = None
    
    def send_image_to_qlab(self, image_path: str, cue_name: Optional[str] = None) -> bool:
        """Send image to QLab using AppleScript"""
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return False
        
        # Convert to absolute path
        abs_image_path = os.path.abspath(image_path)
        
        # Generate cue name if not provided
        if not cue_name:
            filename = os.path.basename(image_path)
            cue_name = f"AI Background - {filename}"
        
        # AppleScript to create new video cue in QLab
        applescript = f'''
        tell application "QLab"
            tell front workspace
                -- Create new video cue (handles images)
                set newCue to make type "Video"
                
                -- Set the file path
                set file target of newCue to "{abs_image_path}"
                
                -- Set cue name
                set q name of newCue to "{cue_name}"
                
                -- Start the cue
                start newCue
                
                return q name of newCue
            end tell
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"Successfully sent image to QLab: {cue_name}")
                return True
            else:
                print(f"QLab AppleScript error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("QLab AppleScript timed out")
            return False
        except Exception as e:
            print(f"Error sending to QLab: {e}")
            return False
    
    def create_and_start_video_cue(self, image_path: str, duration: int = 10) -> bool:
        """Alternative method to create and immediately start a video cue"""
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return False
        
        # Check if QLab is running by trying to communicate
        try:
            check_script = '''
            tell application "QLab"
                return "running"
            end tell
            '''
            result = subprocess.run(['osascript', '-e', check_script], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("QLab 5 is not running or not responding")
                return False
        except Exception as e:
            print(f"Could not communicate with QLab: {e}")
            return False
        
        abs_image_path = os.path.abspath(image_path)
        filename = os.path.basename(image_path)
        
        # Working approach with optional previous cue stopping
        try:
            # Step 1: Stop previous cue if enabled and exists
            if self.auto_stop_previous and self.last_cue_id:
                stop_script = f'''
tell application "QLab"
    tell front workspace
        tell cue id "{self.last_cue_id}"
            stop
        end tell
    end tell
end tell
                '''
                subprocess.run(['osascript', '-e', stop_script], capture_output=True, text=True, timeout=5)
                print(f"🛑 Stopped previous background")
            
            # Step 2: Create new cue
            create_script = '''
tell application "QLab"
    tell front workspace
        make type "Video"
    end tell
end tell
            '''
            
            result = subprocess.run(['osascript', '-e', create_script], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print(f"QLab create error: {result.stderr}")
                return False
            
            # Step 3: Set properties, get ID, and start
            set_script = f'''
tell application "QLab"
    tell front workspace
        set lastCue to last item of cues
        set file target of lastCue to "{abs_image_path}"
        set q name of lastCue to "AI Background"
        start lastCue
        return uniqueID of lastCue
    end tell
end tell
            '''
            
            result = subprocess.run(['osascript', '-e', set_script], capture_output=True, text=True, timeout=10)
            
            # Store the cue ID for future stopping
            if result.returncode == 0 and result.stdout.strip():
                self.last_cue_id = result.stdout.strip()
                print(f"📝 Stored cue ID: {self.last_cue_id}")
            
            if result.returncode == 0:
                print(f"Created and started QLab cue: {result.stdout.strip()}")
                return True
            else:
                print(f"QLab error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error with QLab: {e}")
            return False
    
    def create_default_backdrop(self) -> bool:
        """Create a neutral default backdrop cue"""
        try:
            # Create a simple fade cue or color wash as default
            create_script = '''
tell application "QLab"
    tell front workspace
        set defaultCue to make type "Fade"
        set q name of defaultCue to "DEFAULT BACKDROP"
        set fade type of defaultCue to fade_out
        set duration of defaultCue to 2
        return uniqueID of defaultCue
    end tell
end tell
            '''
            
            result = subprocess.run(['osascript', '-e', create_script], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                self.default_backdrop_id = result.stdout.strip()
                print(f"🎭 Created default backdrop cue: {self.default_backdrop_id}")
                return True
            else:
                print(f"Failed to create default backdrop: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error creating default backdrop: {e}")
            return False
    
    def go_to_default_backdrop(self) -> bool:
        """Switch to the default backdrop"""
        try:
            # First stop current background if any
            if self.last_cue_id:
                stop_script = f'''
tell application "QLab"
    tell front workspace
        tell cue id "{self.last_cue_id}"
            stop
        end tell
    end tell
end tell
                '''
                subprocess.run(['osascript', '-e', stop_script], capture_output=True, text=True, timeout=5)
                print(f"🛑 Stopped current background")
            
            # Create simple neutral background if no default exists
            if not self.default_backdrop_id:
                self.create_default_backdrop()
            
            # Alternative: Just stop everything and let stage lights handle it
            print(f"🎭 Switched to default backdrop")
            self.last_cue_id = None
            return True
            
        except Exception as e:
            print(f"Error switching to default backdrop: {e}")
            return False