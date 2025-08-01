#!/usr/bin/env python3

import os
import time
import subprocess
from typing import Optional, Dict

class EnvironmentSoundGenerator:
    def __init__(self):
        self.sounds_dir = "generated_sounds"
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # Map environments to sound descriptions
        self.sound_mappings = {
            # Nature environments
            'park': 'gentle birds chirping, distant children playing, soft breeze through trees',
            'forest': 'rustling leaves, distant owl hoots, gentle wind through trees',
            'beach': 'gentle waves lapping, seagulls calling, soft ocean breeze',
            'rain': 'steady rainfall, distant thunder, water droplets',
            
            # Urban environments  
            'city': 'distant traffic hum, occasional car horns, urban ambient noise',
            'street': 'footsteps on pavement, distant conversations, city atmosphere',
            'restaurant': 'quiet conversations, clinking cutlery, gentle background music',
            'coffee_shop': 'espresso machine sounds, quiet chatter, gentle cafe ambiance',
            
            # Indoor environments
            'office': 'quiet keyboard typing, distant phone rings, air conditioning hum',
            'hospital': 'quiet medical equipment beeps, distant announcements, sterile ambiance',
            'library': 'pages turning, quiet whispers, peaceful silence',
            'kitchen': 'sizzling pans, chopping sounds, running water, refrigerator hum',
            'gym': 'weights clanking, treadmill sounds, background workout music',
            'classroom': 'pencils writing, quiet chatter, occasional chair squeaks',
            
            # Special environments
            'castle': 'medieval ambiance, distant wind, echoing footsteps',
            'spaceship': 'gentle electronic hums, computer beeps, futuristic ambiance',
            'underwater': 'bubble sounds, muffled water movement, deep ocean ambiance'
        }
    
    def get_sound_for_environment(self, environment_name: str) -> Optional[str]:
        """Get appropriate sound description for an environment"""
        # Clean environment name
        env_clean = environment_name.lower().replace('_', ' ')
        
        # Check for direct matches first
        for env_key, sound_desc in self.sound_mappings.items():
            if env_key in env_clean:
                return sound_desc
        
        # Check for partial matches
        if 'park' in env_clean or 'garden' in env_clean:
            return self.sound_mappings['park']
        elif 'forest' in env_clean or 'woods' in env_clean or 'tree' in env_clean:
            return self.sound_mappings['forest']
        elif 'beach' in env_clean or 'ocean' in env_clean or 'seaside' in env_clean:
            return self.sound_mappings['beach']
        elif 'rain' in env_clean or 'storm' in env_clean:
            return self.sound_mappings['rain']
        elif 'city' in env_clean or 'urban' in env_clean:
            return self.sound_mappings['city']
        elif any(cuisine in env_clean for cuisine in ['restaurant', 'dining', 'italian', 'chinese', 'mexican', 'thai', 'indian', 'french', 'japanese', 'korean', 'vietnamese', 'greek', 'mediterranean', 'middle_eastern', 'noodle', 'szechuan', 'sushi', 'pizzeria', 'steakhouse', 'bistro']):
            return self.sound_mappings['restaurant']
        elif 'coffee' in env_clean or 'cafe' in env_clean:
            return self.sound_mappings['coffee_shop']
        elif 'office' in env_clean or 'meeting' in env_clean:
            return self.sound_mappings['office']
        elif 'hospital' in env_clean or 'medical' in env_clean or 'surgery' in env_clean:
            return self.sound_mappings['hospital']
        elif 'kitchen' in env_clean:
            return self.sound_mappings['kitchen']
        elif 'gym' in env_clean or 'basketball' in env_clean or 'sports' in env_clean:
            return self.sound_mappings['gym']
        elif 'classroom' in env_clean or 'school' in env_clean:
            return self.sound_mappings['classroom']
        elif 'castle' in env_clean or 'medieval' in env_clean:
            return self.sound_mappings['castle']
        elif 'space' in env_clean or 'ship' in env_clean:
            return self.sound_mappings['spaceship']
        
        return None
    
    def create_ambient_sound_cue(self, environment_name: str) -> bool:
        """Create an ambient sound cue in QLab for the environment"""
        sound_description = self.get_sound_for_environment(environment_name)
        
        if not sound_description:
            print(f"🔇 No ambient sound defined for: {environment_name}")
            return False
        
        print(f"🎵 Adding ambient sound: {sound_description}")
        
        try:
            # Create an audio cue in QLab for ambient sound
            create_sound_script = f'''
tell application "QLab"
    tell front workspace
        set theSoundCue to make type "Audio"
        set q name of theSoundCue to "Ambient: {environment_name}"
        -- Note: You would set the audio file here if available
        -- set file target of theSoundCue to "path/to/ambient/{environment_name}.wav"
        set looping of theSoundCue to true
        set level of theSoundCue to -20
        return uniqueID of theSoundCue
    end tell
end tell
            '''
            
            result = subprocess.run(['osascript', '-e', create_sound_script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"🎵 Created ambient sound cue for {environment_name}")
                return True
            else:
                print(f"Failed to create sound cue: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error creating ambient sound: {e}")
            return False
    
    def generate_simple_ambient_file(self, environment_name: str, duration_seconds: int = 60) -> Optional[str]:
        """Find existing ambient sound file or generate placeholder"""
        sound_description = self.get_sound_for_environment(environment_name)
        
        if not sound_description:
            return None
        
        # Check for existing files with different extensions
        base_filename = f"{environment_name}_ambient"
        possible_files = [
            f"{base_filename}.wav",
            f"{base_filename}.mp3", 
            f"{base_filename}.flac",
            f"{base_filename}.m4a"
        ]
        
        for filename in possible_files:
            filepath = os.path.join(self.sounds_dir, filename)
            if os.path.exists(filepath):
                print(f"🎵 Found ambient sound: {filename}")
                return filepath
        
        print(f"🎵 No ambient sound found for: {environment_name}")
        print(f"   Would use: {sound_description}")
        print(f"   Searched for: {', '.join(possible_files)}")
        
        return None
    
    def show_sound_library(self):
        """Show available environment sounds"""
        print("🎵 Environment Sound Library")
        print("=" * 40)
        
        for env, description in self.sound_mappings.items():
            print(f"🎶 {env}: {description}")

def main():
    """Test the sound generator"""
    generator = EnvironmentSoundGenerator()
    generator.show_sound_library()
    
    # Test some environments
    test_environments = ["park", "coffee_shop", "forest", "hospital"]
    
    print(f"\n🧪 Testing sound mappings:")
    for env in test_environments:
        sound = generator.get_sound_for_environment(env)
        if sound:
            print(f"  {env}: {sound}")
        else:
            print(f"  {env}: No sound mapping")

if __name__ == "__main__":
    main()