#!/usr/bin/env python3

import os
import sys
import time
import signal
from dotenv import load_dotenv
from speech_recognizer import RealTimeSpeechRecognizer
from image_generator import AIImageGenerator
from qlab_integration import QLab

class ImprovAIApp:
    def __init__(self, fast_mode=True):
        # Load environment variables
        load_dotenv()
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("Error: OPENAI_API_KEY not found in .env file")
            sys.exit(1)
        
        # Initialize components (fast mode for speed)
        self.image_generator = AIImageGenerator(self.openai_api_key, fast_mode=fast_mode)
        self.qlab = QLab(auto_stop_previous=True)  # Auto-stop previous backgrounds
        self.speech_recognizer = RealTimeSpeechRecognizer(self.on_speech_recognized)
        
        # State
        self.running = False
        self.last_generation_time = 0
        self.min_interval = 15  # Minimum seconds between generations
        self.fast_mode = fast_mode
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def on_speech_recognized(self, text: str):
        """Callback for when speech is recognized"""
        current_time = time.time()
        
        # Rate limiting to avoid too many generations
        if current_time - self.last_generation_time < self.min_interval:
            print(f"Rate limited - waiting {self.min_interval - (current_time - self.last_generation_time):.1f}s")
            return
        
        # Filter out very short phrases
        if len(text.split()) < 3:
            print(f"Phrase too short, ignoring: '{text}'")
            return
        
        print(f"\n🎭 Heard: '{text}'")
        
        # Generate image (includes location detection)
        generation_start = time.time()
        image_path = self.image_generator.generate_background_image(text)
        
        if image_path:
            generation_time = time.time() - generation_start
            if generation_time < 2:  # Reused from library
                print(f"⚡ Environment loaded instantly (from library)")
            else:  # Newly generated
                mode_text = "fast mode" if self.fast_mode else "high quality"
                print(f"⚡ Generated in {generation_time:.1f}s ({mode_text})")
            
            # Send to QLab
            success = self.qlab.create_and_start_video_cue(image_path, duration=20)
            if success:
                print(f"✅ Background updated in QLab")
                self.last_generation_time = current_time
            else:
                print(f"❌ Failed to update QLab")
        # Note: if image_path is None, location detection already printed the reason
    
    def start(self):
        """Start the application"""
        print("🎭 Improv AI Background Generator (Fast Mode - DALL-E 2)")
        print("=" * 60)
        print("⚡ Using DALL-E 2 for faster generation")
        print("Initializing speech recognition...")
        
        try:
            # Test microphone access first
            import speech_recognition as sr
            r = sr.Recognizer()
            mic = sr.Microphone()
            print("Testing microphone access...")
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone access OK")
            
        except Exception as e:
            print(f"❌ Microphone error: {e}")
            print("Please ensure microphone permissions are granted to Terminal/Python")
            return
        
        print("Listening for speech to generate theater backgrounds...")
        print("Speak phrases like:")
        print("  - 'It's beautiful today in this park'")
        print("  - 'We're in a dark mysterious forest'")
        print("  - 'The city skyline glows at sunset'")
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        self.speech_recognizer.start_listening()
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the application"""
        print("\n🛑 Stopping Improv AI...")
        self.running = False
        self.speech_recognizer.stop_listening_method()
        print("Goodbye!")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.stop()

def main():
    """Main entry point"""
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Creating .env file...")
        print("Please add your OpenAI API key to the .env file:")
        print("OPENAI_API_KEY=your_api_key_here")
        
        with open('.env', 'w') as f:
            f.write('OPENAI_API_KEY=your_openai_api_key_here\n')
        
        print("\n.env file created. Please edit it with your API key and run again.")
        return
    
    # Start the application in FAST mode
    app = ImprovAIApp(fast_mode=True)
    app.start()

if __name__ == "__main__":
    main()