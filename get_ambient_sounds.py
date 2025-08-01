#!/usr/bin/env python3

"""
Helper script to get ambient sound files for theater environments.
This script provides guidance and tools for sourcing ambient audio.
"""

import os
from typing import Dict, List

class AmbientSoundCollector:
    def __init__(self):
        self.sounds_dir = "generated_sounds"
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # Free ambient sound sources and suggestions
        self.sound_sources = {
            "freesound.org": {
                "description": "Large free sound library with Creative Commons sounds",
                "requires": "Free account signup",
                "quality": "High - professional recordings"
            },
            "zapsplat.com": {
                "description": "Professional sound effects library", 
                "requires": "Free account with daily download limits",
                "quality": "Very High - broadcast quality"
            },
            "youtube_audio_library": {
                "description": "YouTube's free audio library",
                "requires": "YouTube account",
                "quality": "High - royalty free"
            },
            "ai_generation": {
                "description": "AI tools like Suno, Udio for custom ambient tracks",
                "requires": "Account with these services",
                "quality": "Variable - can be very good"
            }
        }
        
        # Specific recommendations for each environment
        self.environment_recommendations = {
            "park": {
                "keywords": ["birds chirping", "gentle breeze", "nature ambience", "park sounds"],
                "duration": "30-60 seconds loop",
                "volume": "Soft background level"
            },
            "coffee_shop": {
                "keywords": ["coffee shop ambience", "espresso machine", "quiet chatter", "cafe sounds"],
                "duration": "60+ seconds loop", 
                "volume": "Medium background level"
            },
            "restaurant": {
                "keywords": ["restaurant ambience", "cutlery clinking", "dining sounds", "background chatter"],
                "duration": "60+ seconds loop",
                "volume": "Medium background level"
            },
            "forest": {
                "keywords": ["forest ambience", "rustling leaves", "woodland sounds", "nature"],
                "duration": "30-60 seconds loop",
                "volume": "Soft background level"
            },
            "beach": {
                "keywords": ["ocean waves", "seagulls", "beach ambience", "wave sounds"],
                "duration": "30-60 seconds loop", 
                "volume": "Medium background level"
            },
            "office": {
                "keywords": ["office ambience", "typing sounds", "air conditioning", "workplace sounds"],
                "duration": "60+ seconds loop",
                "volume": "Very soft background level"
            },
            "city": {
                "keywords": ["city ambience", "traffic distant", "urban sounds", "street noise"],
                "duration": "60+ seconds loop",
                "volume": "Medium background level"
            },
            "rain": {
                "keywords": ["rain sounds", "rainfall", "storm ambience", "weather sounds"],
                "duration": "30-60 seconds loop",
                "volume": "Medium background level"
            }
        }

    def show_recommendations(self):
        """Show sound sourcing recommendations"""
        print("🎵 Ambient Sound Collection Guide")
        print("=" * 50)
        
        print("\n📚 Recommended Sources:")
        for source, info in self.sound_sources.items():
            print(f"\n🎶 {source}")
            print(f"   Description: {info['description']}")
            print(f"   Requirements: {info['requires']}")
            print(f"   Quality: {info['quality']}")
        
        print("\n🎭 Environment-Specific Recommendations:")
        print("-" * 40)
        
        for env, rec in self.environment_recommendations.items():
            print(f"\n🎵 {env.upper()}")
            print(f"   Search keywords: {', '.join(rec['keywords'])}")
            print(f"   Duration: {rec['duration']}")
            print(f"   Volume level: {rec['volume']}")
    
    def create_sound_collection_plan(self):
        """Create a plan for collecting sounds"""
        print("\n📋 Sound Collection Action Plan:")
        print("=" * 40)
        
        priority_environments = ["park", "coffee_shop", "restaurant", "office", "forest", "city"]
        
        print("🎯 Priority 1 - Essential Environments:")
        for env in priority_environments:
            if env in self.environment_recommendations:
                rec = self.environment_recommendations[env]
                print(f"  □ {env}: Search for '{rec['keywords'][0]}'")
        
        print("\n🎯 Priority 2 - Extended Environments:")
        remaining = [env for env in self.environment_recommendations.keys() if env not in priority_environments]
        for env in remaining:
            rec = self.environment_recommendations[env]
            print(f"  □ {env}: Search for '{rec['keywords'][0]}'")
        
        print(f"\n📁 Save files to: {os.path.abspath(self.sounds_dir)}")
        print("📝 File naming: environment_ambient.wav (e.g., park_ambient.wav)")
        print("\n💡 Tips:")
        print("  • Look for seamless loops")
        print("  • Prefer .wav or .mp3 format")
        print("  • Keep files under 5MB for QLab performance")
        print("  • Test volume levels in QLab before show")

    def check_existing_sounds(self):
        """Check what sounds are already available"""
        print(f"\n📂 Checking existing sounds in {self.sounds_dir}...")
        
        if not os.path.exists(self.sounds_dir):
            print("  No sounds directory found")
            return
        
        sound_files = [f for f in os.listdir(self.sounds_dir) if f.endswith(('.wav', '.mp3', '.m4a', '.aiff'))]
        
        if sound_files:
            print(f"  Found {len(sound_files)} sound files:")
            for file in sorted(sound_files):
                env_name = file.split('_')[0] if '_' in file else file.split('.')[0]
                print(f"    ✅ {file} ({env_name})")
        else:
            print("  No sound files found")
        
        # Show what's missing
        all_environments = list(self.environment_recommendations.keys())
        found_environments = [f.split('_')[0] for f in sound_files if '_' in f]
        missing = [env for env in all_environments if env not in found_environments]
        
        if missing:
            print(f"\n❌ Missing sounds for: {', '.join(missing)}")
        else:
            print(f"\n✅ Have sounds for all environments!")

def main():
    """Main function to run the ambient sound collection guide"""
    collector = AmbientSoundCollector()
    
    print("🎭 Improv AI - Ambient Sound Collection Tool")
    print("=" * 50)
    
    collector.check_existing_sounds()
    collector.show_recommendations()
    collector.create_sound_collection_plan()
    
    print("\n🚀 Next Steps:")
    print("1. Visit freesound.org or zapsplat.com")
    print("2. Search for the recommended keywords")
    print("3. Download and save to generated_sounds/ folder")
    print("4. Test in QLab before your show")
    print("5. Run 'python test_sounds.py' to verify integration")

if __name__ == "__main__":
    main()