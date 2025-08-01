#!/usr/bin/env python3

import os
import time
from qlab_integration import QLab

def demo_workflow():
    """Demo the workflow without API calls"""
    print("🎭 Improv AI Background Generator - DEMO MODE")
    print("=" * 50)
    print("(This demo shows the workflow without API calls)")
    print()
    
    qlab = QLab()
    
    # Demo phrases and their mock generated backgrounds
    demo_scenarios = [
        {
            "speech": "It's a beautiful day in the park",
            "enhanced_prompt": "Sunny park scene with green grass, blooming flowers, blue sky, soft shadows from trees, peaceful atmosphere, theatrical lighting, professional theater backdrop, wide angle, high quality, dramatic atmosphere",
            "mock_image": "beautiful_park_background.jpg"
        },
        {
            "speech": "We're in a dark mysterious forest",
            "enhanced_prompt": "Dark mysterious forest with tall shadowy trees, dappled moonlight filtering through branches, misty atmosphere, deep shadows, eerie but beautiful, theatrical lighting, professional theater backdrop, wide angle, high quality, dramatic atmosphere",
            "mock_image": "mysterious_forest_background.jpg"
        },
        {
            "speech": "The city skyline glows at sunset",
            "enhanced_prompt": "Urban city skyline at golden hour sunset, warm orange and pink sky, silhouetted buildings, glowing windows, dramatic clouds, cinematic atmosphere, theatrical lighting, professional theater backdrop, wide angle, high quality, dramatic atmosphere",
            "mock_image": "sunset_city_background.jpg"
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"🎪 Demo {i}/3: Actor says '{scenario['speech']}'")
        print(f"🧠 AI enhances to: {scenario['enhanced_prompt'][:80]}...")
        print(f"🖼️  Generating image: {scenario['mock_image']}")
        
        # Simulate generation time
        for j in range(3):
            print("   .", end="", flush=True)
            time.sleep(0.5)
        print(" ✅")
        
        # Test QLab connection (will fail gracefully if QLab not running)
        print("📺 Attempting to send to QLab...")
        if os.path.exists("/Applications/QLab 5.app") or os.path.exists("/Applications/QLab 4.app"):
            print("   QLab detected but no actual image to send in demo mode")
            print("   ✅ Would create video cue and start playback")
        else:
            print("   ⚠️  QLab not installed (install from figure53.com)")
        
        print(f"🎬 Background would now be displayed for 20 seconds")
        
        if i < len(demo_scenarios):
            print("\n" + "-" * 40 + "\n")
    
    print("\n🎉 Demo complete!")
    print("\nTo use with real AI generation:")
    print("1. Add payment method to OpenAI account")
    print("2. Run: python main.py")
    print("3. Make sure QLab is running")
    print("4. Start speaking your improv lines!")

if __name__ == "__main__":
    demo_workflow()