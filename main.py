#!/usr/bin/env python3

import os
import sys
import time
import signal
from dotenv import load_dotenv
from speech_recognizer import RealTimeSpeechRecognizer
from image_generator import AIImageGenerator
from qlab_integration import QLab
from sound_generator import EnvironmentSoundGenerator

class ImprovAIApp:
    def __init__(self, fast_mode=False, auto_default_after_minutes=None, enable_ambient_sounds=True):
        # Load environment variables
        load_dotenv()
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("Error: OPENAI_API_KEY not found in .env file")
            sys.exit(1)
        
        # Initialize components (default to DALL-E 3 for quality)
        self.image_generator = AIImageGenerator(self.openai_api_key, fast_mode=fast_mode)
        self.qlab = QLab(auto_stop_previous=True)  # Auto-stop previous backgrounds
        self.sound_generator = EnvironmentSoundGenerator()
        self.speech_recognizer = RealTimeSpeechRecognizer(self.on_speech_recognized)
        
        # State
        self.running = False
        self.last_generation_time = 0
        self.last_activity_time = time.time()
        self.min_interval = 15  # Minimum seconds between generations
        self.fast_mode = fast_mode
        self.auto_default_after_minutes = auto_default_after_minutes
        self.last_default_check = time.time()
        self.enable_ambient_sounds = enable_ambient_sounds
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def on_speech_recognized(self, text: str):
        """Callback for when speech is recognized"""
        current_time = time.time()
        
        # Filter out very short phrases
        if len(text.split()) < 3:
            print(f"Phrase too short, ignoring: '{text}'")
            return
        
        print(f"\n🎭 Heard: '{text}'")
        
        # Generate image (includes location detection and smart rate limiting)
        generation_start = time.time()
        
        # Pass rate limiting info to the image generator
        time_since_last_generation = current_time - self.last_generation_time
        result = self.image_generator.generate_background_image(
            text, 
            min_interval=self.min_interval,
            time_since_last=time_since_last_generation
        )
        
        if result:
            image_path, was_reused = result if isinstance(result, tuple) else (result, False)
            generation_time = time.time() - generation_start
            
            if was_reused:
                print(f"⚡ Environment loaded instantly (from library)")
            else:
                mode_text = "fast mode" if self.fast_mode else "high quality"
                print(f"⚡ Generated in {generation_time:.1f}s ({mode_text})")
            
            # Send to QLab
            success = self.qlab.create_and_start_video_cue(image_path, duration=20)
            if success:
                print(f"✅ Background updated in QLab")
                
                # Add ambient sound for the environment (if enabled)
                if self.enable_ambient_sounds:
                    environment_name = os.path.basename(image_path).replace('.png', '')
                    self.sound_generator.create_ambient_sound_cue(environment_name)
                
                # Only update rate limiting time for actual generations, not library reuse
                if not was_reused:
                    self.last_generation_time = current_time
                self.last_activity_time = current_time  # Update activity time
            else:
                print(f"❌ Failed to update QLab")
        # Note: if image_path is None, location detection already printed the reason
    
    def start(self):
        """Start the application"""
        mode_name = "Fast Mode (DALL-E 2)" if self.fast_mode else "High Quality (DALL-E 3)"
        print(f"🎭 Improv AI Background Generator ({mode_name})")
        print("=" * 60)
        if self.fast_mode:
            print("⚡ Using DALL-E 2 for faster generation")
        else:
            print("🎨 Using DALL-E 3 for high quality backgrounds")
        
        if self.enable_ambient_sounds:
            print("🎵 Ambient sounds enabled")
        else:
            print("🔇 Ambient sounds disabled")
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
                
                # Check for auto-default backdrop
                if self.auto_default_after_minutes:
                    current_time = time.time()
                    time_since_activity = (current_time - self.last_activity_time) / 60  # minutes
                    time_since_check = current_time - self.last_default_check
                    
                    # Check every 30 seconds and if enough time has passed since last activity
                    if time_since_check > 30 and time_since_activity >= self.auto_default_after_minutes:
                        print(f"\n⏰ No activity for {self.auto_default_after_minutes} minutes - switching to default backdrop")
                        self.qlab.go_to_default_backdrop()
                        self.last_default_check = current_time
                        self.last_activity_time = current_time  # Reset to avoid repeated triggers
                        
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
    import argparse
    
    parser = argparse.ArgumentParser(description='🎭 Improv AI - Real-time theater background generator')
    parser.add_argument('--fast', action='store_true', help='Use DALL-E 2 for faster generation')
    parser.add_argument('--no-sounds', action='store_true', help='Disable ambient sound generation')
    parser.add_argument('--auto-default', type=int, metavar='MINUTES', 
                       help='Auto-trigger default backdrop after N minutes of inactivity')
    
    args = parser.parse_args()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Creating .env file...")
        print("Please add your OpenAI API key to the .env file:")
        print("OPENAI_API_KEY=your_api_key_here")
        
        with open('.env', 'w') as f:
            f.write('OPENAI_API_KEY=your_openai_api_key_here\n')
        
        print("\n.env file created. Please edit it with your API key and run again.")
        return
    
    # Start the application with options
    app = ImprovAIApp(
        fast_mode=args.fast,
        auto_default_after_minutes=args.auto_default,
        enable_ambient_sounds=not args.no_sounds
    )
    app.start()

if __name__ == "__main__":
    main()