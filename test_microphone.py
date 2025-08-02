#!/usr/bin/env python3

"""
Microphone test utility for Improv AI
Helps users test and optimize their microphone setup
"""

import speech_recognition as sr
import numpy as np
import time
import sys

def test_microphone():
    """Test microphone and provide setup recommendations"""
    print("🎤 Improv AI - Microphone Test Utility")
    print("=" * 50)
    
    recognizer = sr.Recognizer()
    
    # List available microphones
    print("\n📋 Available microphones:")
    mic_list = sr.Microphone.list_microphone_names()
    for i, mic_name in enumerate(mic_list):
        print(f"   [{i}] {mic_name}")
    
    # Let user select microphone
    if len(mic_list) > 1:
        print("\nWhich microphone to use? (Enter number or press Enter for default): ", end='')
        try:
            choice = input().strip()
            if choice:
                device_index = int(choice)
                microphone = sr.Microphone(device_index=device_index)
                print(f"✅ Using: {mic_list[device_index]}")
            else:
                microphone = sr.Microphone()
                print("✅ Using default microphone")
        except:
            microphone = sr.Microphone()
            print("✅ Using default microphone")
    else:
        microphone = sr.Microphone()
    
    # Test ambient noise
    print("\n🔊 Testing ambient noise level...")
    print("   Please remain quiet for 5 seconds...")
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
    
    noise_level = recognizer.energy_threshold
    print(f"\n📊 Ambient noise level: {noise_level:.0f}")
    
    if noise_level < 100:
        print("   ✅ Very quiet environment - excellent!")
    elif noise_level < 300:
        print("   ✅ Good - low background noise")
    elif noise_level < 1000:
        print("   ⚠️ Moderate noise - speech recognition may need louder voice")
    else:
        print("   ❌ High noise level - consider:")
        print("      • Moving to a quieter location")
        print("      • Using a directional microphone")
        print("      • Closing windows/doors")
    
    # Test speech recognition
    print("\n🎭 Testing speech recognition...")
    print("=" * 50)
    
    test_phrases = [
        "Let's go to the coffee shop",
        "We're in a beautiful park today",
        "This Italian restaurant is amazing",
        "Welcome to our office meeting"
    ]
    
    print("\nPlease speak the following phrases clearly:")
    print("(Press Ctrl+C to skip any phrase)\n")
    
    successful_recognitions = 0
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n[{i}/4] Please say: \"{phrase}\"")
        print("Listening... ", end='', flush=True)
        
        try:
            with microphone as source:
                # Listen for up to 10 seconds
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            # Try to recognize
            try:
                recognized = recognizer.recognize_google(audio)
                print(f"\n✅ Recognized: \"{recognized}\"")
                
                # Check accuracy
                if recognized.lower().strip() == phrase.lower().strip():
                    print("   Perfect match!")
                    successful_recognitions += 1
                else:
                    # Calculate similarity
                    recognized_words = set(recognized.lower().split())
                    expected_words = set(phrase.lower().split())
                    common_words = recognized_words.intersection(expected_words)
                    accuracy = len(common_words) / len(expected_words) * 100
                    
                    print(f"   Accuracy: {accuracy:.0f}%")
                    if accuracy >= 70:
                        successful_recognitions += 1
                        
            except sr.UnknownValueError:
                print("\n❌ Could not understand audio")
                print("   Try speaking louder or more clearly")
                
        except sr.WaitTimeoutError:
            print("\n⏱️ Timeout - no speech detected")
        except KeyboardInterrupt:
            print("\n⏭️ Skipped")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Final recommendations
    print("\n" + "=" * 50)
    print("📊 Test Results")
    print("=" * 50)
    
    success_rate = (successful_recognitions / len(test_phrases)) * 100
    print(f"\nRecognition success rate: {success_rate:.0f}%")
    
    if success_rate >= 75:
        print("✅ Excellent! Your microphone setup is ready for Improv AI")
    elif success_rate >= 50:
        print("⚠️ Good, but could be better. Consider:")
        print("   • Speaking more clearly and at consistent volume")
        print("   • Getting closer to the microphone")
        print("   • Reducing background noise")
    else:
        print("❌ Poor recognition quality. Recommendations:")
        print("   • Check microphone connection")
        print("   • Increase microphone gain/volume in system settings")
        print("   • Use a better quality microphone")
        print("   • Move to a quieter environment")
        print("   • Speak louder and more clearly")
    
    print("\n💡 Tips for best results during performances:")
    print("   • Maintain consistent distance from microphone")
    print("   • Speak clearly without rushing")
    print("   • Project your voice as in normal theater performance")
    print("   • Test again if you change locations or microphones")

if __name__ == "__main__":
    try:
        test_microphone()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have installed all dependencies:")
        print("  pip install speechrecognition pyaudio")