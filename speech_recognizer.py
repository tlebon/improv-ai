import speech_recognition as sr
import pyaudio
import threading
import queue
import time
from typing import Callable, Optional

class RealTimeSpeechRecognizer:
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        self.stop_listening = None
        self.is_running = False
        self.error_count = 0
        
        # Enhanced recognizer settings for better quality
        self.recognizer.energy_threshold = 300  # Base energy threshold
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust for room noise
        self.recognizer.dynamic_energy_adjustment_damping = 0.15  # Slower adjustment
        self.recognizer.dynamic_energy_ratio = 1.5  # Less aggressive cutoff
        self.recognizer.pause_threshold = 1.5  # Wait 1.5s of silence before ending
        self.recognizer.non_speaking_duration = 0.5  # Min silence duration
        self.recognizer.operation_timeout = None  # No timeout
        
        # Better calibration
        print("🎙️ Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=3)
        print(f"✅ Calibration complete. Noise level: {self.recognizer.energy_threshold:.0f}")
    
    def start_listening(self):
        """Start continuous speech recognition"""
        if self.is_running:
            return
        
        self.is_running = True
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self._audio_callback,
            phrase_time_limit=15  # Even longer for theater dialogue
        )
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._process_audio)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        print("Started listening for speech...")
    
    def stop_listening_method(self):
        """Stop speech recognition"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        print("Stopped listening for speech.")
    
    def _audio_callback(self, recognizer, audio):
        """Callback for when audio is detected"""
        self.audio_queue.put(audio)
    
    def _process_audio(self):
        """Process audio from the queue with enhanced recognition"""
        consecutive_errors = 0
        
        while self.is_running:
            try:
                audio = self.audio_queue.get(timeout=1)
                
                # Try recognition with better error handling
                try:
                    # Primary attempt with standard settings
                    text = self.recognizer.recognize_google(audio, language="en-US")
                    if text.strip():
                        print(f"Recognized: {text}")
                        self.callback(text)
                        consecutive_errors = 0  # Reset on success
                        continue
                except sr.UnknownValueError:
                    # Try with show_all for alternatives
                    try:
                        result = self.recognizer.recognize_google(audio, show_all=True)
                        if result and isinstance(result, dict) and 'alternative' in result:
                            alternatives = result.get('alternative', [])
                            if alternatives and alternatives[0].get('transcript'):
                                text = alternatives[0]['transcript']
                                confidence = alternatives[0].get('confidence', 1.0)
                                if text.strip():
                                    if confidence < 0.8:
                                        print(f"Recognized (low confidence): {text}")
                                    else:
                                        print(f"Recognized: {text}")
                                    self.callback(text)
                                    consecutive_errors = 0
                                    continue
                    except:
                        pass
                
                # Recognition failed
                consecutive_errors += 1
                self.error_count += 1
                
                # Provide helpful feedback
                if consecutive_errors == 3:
                    print("🎤 Having trouble hearing. Tips:")
                    print("   • Speak louder and clearer")
                    print("   • Get closer to the microphone")
                    print("   • Reduce background noise")
                elif consecutive_errors == 10:
                    print("⚠️ Consistent issues detected - consider restarting")
                elif self.error_count % 10 == 0:
                    print(f"🔇 Audio unclear (shown every 10 attempts)")
                    
            except queue.Empty:
                continue
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                print("   Check internet connection")
                consecutive_errors += 1
            except Exception as e:
                print(f"Unexpected error: {e}")