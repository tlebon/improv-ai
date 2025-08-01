# 🎭 Improv AI - Real-Time Theater Background Generator

An AI-powered system that listens to improv performers in real-time, detects location context from speech, generates appropriate background images, and automatically sends them to QLab for display. Perfect for improv theaters wanting dynamic, responsive backdrops.

## ✨ Features

- **🎤 Real-time speech recognition** - Listens to performers via microphone
- **🧠 AI location detection** - Identifies settings from natural speech 
- **🎨 Dynamic image generation** - Creates backgrounds using DALL-E 3
- **📚 Smart library system** - Reuses existing environments for speed
- **🎵 Ambient sound integration** - Adds appropriate audio atmospheres
- **🎬 QLab automation** - Seamlessly integrates with theater tech setup
- **⚡ Intelligent rate limiting** - Optimized for live performance

## 🚀 Quick Start

### Prerequisites

- **macOS** (for QLab integration)
- **Python 3.8+**
- **QLab 5** (theater lighting/sound software)
- **OpenAI API key** with DALL-E access
- **Microphone** for speech input

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/improv-ai.git
   cd improv-ai
   ```

2. **Set up Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Set up QLab:**
   - Open QLab 5
   - Enable OSC in QLab preferences
   - Create a new workspace for your show

6. **Add ambient sounds (optional):**
   ```bash
   python3 get_ambient_sounds.py  # See guide for sound sources
   ```

### Usage

1. **Start the system:**
   ```bash
   python3 main.py                    # Full features (DALL-E 3 + ambient sounds)
   python3 main.py --fast             # Faster generation (DALL-E 2)
   python3 main.py --no-sounds        # Disable ambient sounds
   python3 main.py --auto-default 5   # Auto-default backdrop after 5min
   ```

2. **Begin your improv performance!** The system will:
   - Listen for location mentions ("Let's go to the coffee shop")
   - Generate or reuse appropriate backgrounds
   - Send images to QLab automatically
   - Add ambient sound cues (if enabled)

3. **Tech controls:**
   - Press `d` + Enter to trigger default backdrop
   - Ctrl+C to exit gracefully

## 🎭 How It Works

### Speech Detection
The system uses Python's SpeechRecognition library to continuously listen for speech patterns that indicate location changes:

```python
# Examples of detected phrases:
"Let's go to the Italian restaurant"    → italian_restaurant.png
"We're at the park now"                → park.png  
"This coffee shop is crowded"          → coffee_shop.png
"Welcome to our office"                → office.png
```

### Location Intelligence
AI analyzes speech context to extract reusable environment names:
- "Fancy Italian bistro" → `italian_restaurant` 
- "Szechuan noodle place" → `chinese_restaurant`
- "Dark spooky forest" → `dark_forest`

### Image Generation
- **First mention**: Generates new DALL-E 3 image (high quality)
- **Subsequent mentions**: Instantly reuses from library
- **Optimized prompts**: Creates intimate, theater-appropriate backgrounds

### QLab Integration
Automatically creates and triggers QLab cues via AppleScript:
- Video cues for background images
- Audio cues for ambient sounds
- Auto-stops previous backgrounds

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=your_api_key_here
```

### Customization Options
- **Rate limiting**: Adjust `min_interval` in `main.py` (default: 15 seconds)
- **Image quality**: Use `--fast` flag for DALL-E 2 vs DALL-E 3 (default)
- **Ambient sounds**: Use `--no-sounds` flag to disable audio cues
- **Auto-default**: Use `--auto-default N` for backdrop after N minutes
- **Speech sensitivity**: Modify `phrase_time_limit` in `speech_recognizer.py`

## 📁 Project Structure

```
improv-ai/
├── main.py                 # Main application orchestrator
├── speech_recognizer.py    # Real-time speech recognition
├── image_generator.py      # AI image generation & library
├── sound_generator.py      # Ambient sound system
├── qlab_integration.py     # QLab AppleScript automation
├── get_ambient_sounds.py   # Sound collection utility
├── generated_images/       # Environment image library
├── generated_sounds/       # Ambient audio files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎵 Adding Ambient Sounds

The system supports ambient audio for immersive environments:

1. **Run the sound collection guide:**
   ```bash
   python3 get_ambient_sounds.py
   ```

2. **Download sounds from:**
   - [Freesound.org](https://freesound.org) (free, Creative Commons)
   - [Zapsplat.com](https://zapsplat.com) (professional quality)
   - YouTube Audio Library
   - AI generation tools (Suno, Udio)

3. **Save as:** `environment_ambient.wav` in `generated_sounds/`
   - `park_ambient.wav`
   - `restaurant_ambient.wav`
   - `coffee_shop_ambient.wav`
   - etc.

## 🎬 Theater Integration Tips

### For Tech Operators
- Set up QLab workspace before show
- Test speech recognition levels during sound check
- Use default backdrop feature (`d` + Enter) between scenes
- Monitor rate limiting - system prevents API spam

### For Performers  
- Speak naturally - system detects context, not commands
- Be specific about locations: "Italian restaurant" vs just "restaurant"
- Allow ~3 seconds for new environments to generate
- Library reuse is instant for repeated locations

### Performance Optimization
- **Internet required** for new image generation
- **Offline capable** for library reuse
- **15-second rate limit** prevents API overuse
- **Smart caching** balances quality with speed

## 🛠️ Troubleshooting

### Common Issues

**"Could not understand speech"**
- Check microphone permissions
- Reduce background noise
- Adjust `phrase_time_limit` in speech_recognizer.py

**"QLab connection failed"**  
- Ensure QLab 5 is running
- Enable OSC in QLab preferences
- Check that workspace is open

**"OpenAI API error"**
- Verify API key in `.env` file
- Check API quota/billing
- Ensure DALL-E access is enabled

**Images too large/small**
- Modify prompt generation in `image_generator.py`
- Adjust QLab video cue settings
- Check theater projector resolution

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional ambient sound mappings
- Enhanced location detection
- Support for other theater software
- Multi-language speech recognition
- Custom prompt templates

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎭 Credits

Created for improv theater communities. Special thanks to:
- OpenAI for DALL-E API
- Figure 53 for QLab
- The improv community for inspiration

## 🔗 Links

- [QLab by Figure 53](https://qlab.app/)
- [OpenAI DALL-E](https://openai.com/dall-e-3)
- [Freesound.org](https://freesound.org) - Ambient sounds
- [Python SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

---

*Made with ❤️ for the theater community*