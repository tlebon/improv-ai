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
        
        # Optimize recognizer settings for theater environment
        self.recognizer.energy_threshold = 300  # Lower for quieter speech
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0  # Longer pause before ending phrase
        self.recognizer.operation_timeout = None  # No timeout
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
    
    def start_listening(self):
        """Start continuous speech recognition"""
        if self.is_running:
            return
        
        self.is_running = True
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self._audio_callback,
            phrase_time_limit=10  # Longer phrases for full sentences
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
        """Process audio from the queue"""
        while self.is_running:
            try:
                audio = self.audio_queue.get(timeout=1)
                text = self.recognizer.recognize_google(audio)
                if text.strip():
                    print(f"Recognized: {text}")
                    self.callback(text)
            except queue.Empty:
                continue
            except sr.UnknownValueError:
                # Could not understand audio - only show occasionally
                self.error_count += 1
                if self.error_count % 10 == 0:  # Show every 10th error
                    print(f"🔇 Audio unclear (shown every 10 attempts)")
                    print("💡 Try speaking louder and more clearly")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")