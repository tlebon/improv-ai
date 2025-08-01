#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from image_generator import AIImageGenerator
from qlab_integration import QLab

def test_image_generation():
    """Test image generation without speech recognition"""
    load_dotenv()
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    print("🎭 Testing Improv AI Background Generator")
    print("=" * 40)
    
    # Initialize components
    image_generator = AIImageGenerator(openai_api_key)
    qlab = QLab()
    
    # Test phrases
    test_phrases = [
        "It's a beautiful day in the park",
        "We're in a dark mysterious forest",
        "The city skyline glows at sunset"
    ]
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n🎪 Test {i}/3: '{phrase}'")
        
        # Generate image
        image_path = image_generator.generate_background_image(phrase)
        
        if image_path:
            print(f"✅ Image generated: {image_path}")
            
            # Try to send to QLab
            success = qlab.create_and_start_video_cue(image_path, duration=5)
            if success:
                print(f"✅ Sent to QLab successfully")
            else:
                print(f"⚠️  QLab not available (check if QLab is running)")
        else:
            print(f"❌ Failed to generate image")
        
        if i < len(test_phrases):
            input("Press Enter for next test...")
    
    print("\n🎉 Test complete!")

if __name__ == "__main__":
    test_image_generation()