#!/usr/bin/env python3

"""
Test script for ambient sound system
"""

from sound_generator import EnvironmentSoundGenerator

def main():
    print("🎵 Testing Ambient Sound System")
    print("=" * 40)
    
    generator = EnvironmentSoundGenerator()
    
    # Show available sounds
    generator.show_sound_library()
    
    print(f"\n🧪 Testing Environment Sound Mapping:")
    print("-" * 40)
    
    test_environments = [
        "park", "coffee_shop", "forest_dark", "hospital_surgery", 
        "castle_courtyard", "beach_day", "rain_storm", "office_meeting",
        "restaurant_italian", "city_street", "spaceship_interior"
    ]
    
    for env in test_environments:
        sound_desc = generator.get_sound_for_environment(env)
        if sound_desc:
            print(f"🎶 {env}")
            print(f"   → {sound_desc}")
        else:
            print(f"🔇 {env} → No sound mapping")
        print()
    
    print("💡 Note: Actual audio files would need to be:")
    print("   1. Created/sourced for each environment")
    print("   2. Placed in QLab workspace")
    print("   3. Referenced in the audio cue creation")
    print("\n🎭 For live theater, consider:")
    print("   • Using royalty-free ambient sound libraries")
    print("   • Recording custom ambient tracks")
    print("   • Using AI music generation services")

if __name__ == "__main__":
    main()