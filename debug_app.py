#!/usr/bin/env python3

import os
import sys
import time
from dotenv import load_dotenv

def test_components():
    """Test each component individually"""
    print("🎭 Improv AI - Component Testing")
    print("=" * 40)
    
    # Test 1: Environment
    print("1. Testing environment...")
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"   ✅ OpenAI API key found (ends with: ...{api_key[-4:]})")
    else:
        print("   ❌ No OpenAI API key in .env")
        return
    
    # Test 2: Imports
    print("2. Testing imports...")
    try:
        import speech_recognition as sr
        print("   ✅ SpeechRecognition imported")
    except ImportError as e:
        print(f"   ❌ SpeechRecognition error: {e}")
        return
    
    try:
        import pyaudio
        print("   ✅ PyAudio imported")
    except ImportError as e:
        print(f"   ❌ PyAudio error: {e}")
        return
    
    try:
        import openai
        print("   ✅ OpenAI imported")
    except ImportError as e:
        print(f"   ❌ OpenAI error: {e}")
        return
    
    # Test 3: Microphone
    print("3. Testing microphone access...")
    try:
        r = sr.Recognizer()
        print("   ✅ Recognizer created")
        
        # List microphones
        mic_list = sr.Microphone.list_microphone_names()
        print(f"   📱 Found {len(mic_list)} microphones")
        for i, name in enumerate(mic_list[:3]):  # Show first 3
            print(f"      {i}: {name}")
        
        # Test default microphone
        mic = sr.Microphone()
        print("   ✅ Default microphone accessible")
        
        # Quick ambient noise test (this might hang if no permissions)
        print("   🎤 Testing ambient noise detection (5 seconds)...")
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
        print("   ✅ Microphone permissions OK")
        
    except Exception as e:
        print(f"   ❌ Microphone error: {e}")
        print("   💡 Grant microphone permissions to Terminal in System Preferences")
        return
    
    # Test 4: OpenAI API
    print("4. Testing OpenAI API...")
    try:
        client = openai.OpenAI(api_key=api_key)
        # Try a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        print("   ✅ OpenAI API working")
    except Exception as e:
        print(f"   ❌ OpenAI API error: {e}")
        if "billing" in str(e).lower():
            print("   💳 Add payment method at platform.openai.com")
        return
    
    # Test 5: QLab detection
    print("5. Testing QLab...")
    qlab_paths = [
        "/Applications/QLab 5.app",
        "/Applications/QLab 4.app"
    ]
    
    qlab_found = False
    for path in qlab_paths:
        if os.path.exists(path):
            print(f"   ✅ Found {os.path.basename(path)}")
            qlab_found = True
            break
    
    if not qlab_found:
        print("   ⚠️  QLab not found - install from figure53.com")
    
    print("\n🎉 Component testing complete!")
    print("\nIf all tests passed, run: python main.py")

if __name__ == "__main__":
    test_components()