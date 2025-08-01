import openai
import requests
from PIL import Image
import io
import os
from typing import Optional
import time

class AIImageGenerator:
    def __init__(self, api_key: str, fast_mode: bool = True):
        self.client = openai.OpenAI(api_key=api_key)
        self.images_dir = "generated_images"
        self.fast_mode = fast_mode
        os.makedirs(self.images_dir, exist_ok=True)
        self._show_library_stats()
    
    def _show_library_stats(self):
        """Show existing environment library stats"""
        existing_files = [f for f in os.listdir(self.images_dir) if f.endswith('.png')]
        
        if existing_files:
            print(f"📚 Environment Library: {len(existing_files)} backgrounds available")
            # Show a few examples
            examples = sorted(existing_files)[:5]
            for example in examples:
                env_name = example.replace('.png', '').replace('_', ' ')
                print(f"   • {env_name}")
            if len(existing_files) > 5:
                print(f"   ... and {len(existing_files) - 5} more")
        else:
            print("📚 Environment Library: Empty (will build as you perform)")
    
    def detect_location_context(self, speech_text: str) -> bool:
        """Check if speech contains location/setting information worth visualizing"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a location detector for theater backgrounds. 
                        Determine if the given speech mentions or IMPLIES a SPECIFIC LOCATION, SETTING, or ENVIRONMENT that would make a good theater background.
                        
                        RESPOND WITH ONLY "YES" or "NO".
                        
                        YES for: 
                        - Explicit locations: parks, restaurants, forests, cities, beaches, offices, rooms, buildings
                        - Professions that imply locations: doctor (hospital), teacher (classroom), chef (kitchen), pilot (cockpit), farmer (farm)
                        - Activities that imply settings: surgery (operating room), cooking (kitchen), swimming (pool/beach), driving (car/road)
                        - Food/drinks that imply restaurants/cafes: cappuccino, latte, wine, pizza, burger (cafe/restaurant)
                        - Restaurant names/types: Starbucks, McDonald's, Italian restaurant, sushi place, diner
                        - Weather/environmental: storm clouds, rain, snow, sunset, lightning (outdoor scenes)
                        - Situational contexts: courtroom, emergency room, spaceship, dungeon, castle
                        
                        NO for: general conversation, greetings, emotions without clear setting context"""
                    },
                    {
                        "role": "user", 
                        "content": f"Speech: '{speech_text}'"
                    }
                ],
                max_tokens=5,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip().upper()
            return result == "YES"
            
        except Exception as e:
            print(f"Location detection error: {e}")
            # Fallback: check for location/profession/activity keywords
            location_keywords = [
                # Explicit locations
                'park', 'restaurant', 'forest', 'beach', 'office', 'room', 'house', 'store', 'cafe', 'bar', 
                'school', 'hospital', 'airport', 'station', 'street', 'outside', 'inside', 'kitchen', 'bathroom',
                # Professions that imply settings
                'doctor', 'nurse', 'teacher', 'chef', 'pilot', 'farmer', 'lawyer', 'judge', 'mechanic', 'scientist',
                'barista', 'waiter', 'waitress', 'server',
                # Activities that imply settings  
                'surgery', 'operation', 'cooking', 'baking', 'swimming', 'driving', 'flying', 'sailing', 'hiking',
                'ordering', 'menu', 'bill', 'check', 'meeting', 'conference', 'presentation', 'interview',
                'basketball', 'tennis', 'football', 'soccer', 'baseball', 'gym', 'workout', 'exercise', 'sports',
                # Food/drink items that imply restaurants/cafes
                'cappuccino', 'latte', 'espresso', 'coffee', 'tea', 'wine', 'beer', 'cocktail', 'burger', 'pizza',
                'sandwich', 'salad', 'pasta', 'steak', 'dessert', 'appetizer', 'falafel', 'shawarma', 'kebab',
                'tacos', 'burritos', 'sushi', 'ramen', 'noodles', 'soup', 'bread', 'bakery', 'croissant',
                # Common restaurant/chain names
                'starbucks', 'mcdonalds', "mcdonald's", 'subway', 'chipotle', 'taco bell', 'kfc', 'burger king',
                'olive garden', 'applebees', "applebee's", 'chilis', "chili's", 'dennys', "denny's", 'ihop',
                'pizza hut', 'dominos', "domino's", 'papa johns', "papa john's", 'wendy\'s', 'wendys',
                # Generic restaurant types
                'sushi', 'chinese', 'italian', 'mexican', 'thai', 'indian', 'french', 'steakhouse', 'diner',
                'bistro', 'pizzeria', 'bakery', 'delicatessen', 'drive-through', 'drive thru', 'fast food',
                # Weather/environmental contexts
                'storm', 'rain', 'snow', 'sunny', 'cloudy', 'thunder', 'lightning', 'fog', 'wind', 'sunset', 'sunrise',
                # Situational contexts
                'courtroom', 'classroom', 'cockpit', 'farm', 'laboratory', 'garage', 'workshop', 'stage', 'theater'
            ]
            return any(keyword in speech_text.lower() for keyword in location_keywords)
    
    def enhance_prompt_for_background(self, speech_text: str) -> str:
        """Convert speech to optimized background image prompt"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Create intimate theater background prompts that feel like you're INSIDE the location having a conversation.
                        
                        THEATER BACKDROP STYLE - Think "two-person scene":
                        - CLOSE, INTIMATE view - like standing in the space
                        - HUMAN SCALE - not wide establishing shots
                        - CONVERSATION-FRIENDLY - cozy, personal spaces
                        - SIMPLE backgrounds that don't overwhelm the actors
                        
                        AVOID: Wide vistas, dramatic landscapes, aerial views, huge spaces, crowds of people, "sweeping" anything
                        USE: Close views, intimate corners, cozy spaces, human-scale environments
                        
                        Examples:
                        Park → "cozy park bench area with nearby trees, intimate garden corner"
                        Restaurant → "intimate restaurant booth with warm lighting, close table setting"
                        Office → "small office space with desk and chair, personal workspace"
                        
                        Keep it under 60 words, focused on the immediate, intimate space around the actors."""
                    },
                    {
                        "role": "user",
                        "content": f"Speech: '{speech_text}'\n\nCreate a location background image prompt:"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            enhanced_prompt = response.choices[0].message.content.strip()
            # Add intimate styling without theater references
            final_prompt = f"{enhanced_prompt}, close-up view, human scale, cozy atmosphere, warm natural lighting, simple background, conversation-friendly space"
            
            print(f"Enhanced prompt: {final_prompt}")
            return final_prompt
            
        except Exception as e:
            print(f"Error enhancing prompt: {e}")
            # Fallback to basic enhancement
            return f"Location scene: {speech_text}, natural lighting, realistic view, everyday setting"
    
    def _extract_environment_name(self, speech_text: str) -> str:
        """Extract the core environment/location for reusable library naming"""
        try:
            # Use AI to extract the core environment concept
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Extract the core ENVIRONMENT/LOCATION from the speech for a theater background library.
                        
                        Return 1-3 words describing the location type, separated by underscores.
                        Include CUISINE/STYLE for restaurants and KEY DESCRIPTORS for unique places.
                        
                        Examples:
                        "wow can you believe that's the pyramids of Giza" → "pyramids_giza"
                        "I'm so glad we finally made it to London" → "london_street" 
                        "can you believe this falafel stand" → "middle_eastern_food"
                        "thanks for coming to this meeting" → "office"
                        "it's snowing outside" → "snowy_landscape"
                        "beautiful day at the beach" → "beach"
                        "we're in a dark forest" → "dark_forest"
                        "let's get coffee" → "coffee_shop"
                        "Szechuan noodle place" → "chinese_restaurant"
                        "Italian restaurant" → "italian_restaurant"
                        "this Mexican place" → "mexican_restaurant"
                        "fancy steakhouse" → "upscale_restaurant"
                        "McDonald's drive-through" → "fast_food"
                        "play basketball" → "basketball_court"
                        "hospital emergency room" → "emergency_room"
                        "old castle courtyard" → "castle_courtyard"
                        "modern art gallery" → "art_gallery"
                        
                        BALANCE specificity with reusability - different cuisine types should get different backgrounds.
                        
                        Keep it descriptive but reusable."""
                    },
                    {
                        "role": "user",
                        "content": f"Speech: '{speech_text}'"
                    }
                ],
                max_tokens=20,
                temperature=0.3
            )
            
            environment = response.choices[0].message.content.strip()
            
            # Clean up the response
            import re
            environment = re.sub(r'[^a-zA-Z0-9_]', '_', environment.lower())
            environment = re.sub(r'_+', '_', environment)  # Remove multiple underscores
            environment = environment.strip('_')  # Remove leading/trailing underscores
            environment = environment[:25]  # Limit length
            
            print(f"🏗️ Environment extracted: '{environment}'")
            return environment
            
        except Exception as e:
            print(f"Environment extraction error: {e}")
            # Fallback: simple keyword extraction
            import re
            words = speech_text.lower().split()
            
            # Key location words that should be preserved with cuisine/style types
            location_words = ['park', 'beach', 'forest', 'office', 'hospital', 'cafe', 'coffee', 
                            'shop', 'store', 'street', 'city', 'london', 'paris', 'giza', 'pyramids',
                            'kitchen', 'bedroom', 'bathroom', 'garage', 'basement', 'attic',
                            'school', 'classroom', 'library', 'airport', 'station', 'hotel',
                            # Restaurant/cuisine types
                            'italian', 'chinese', 'mexican', 'thai', 'indian', 'french', 'japanese',
                            'korean', 'vietnamese', 'greek', 'middle_eastern', 'mediterranean', 
                            'steakhouse', 'bistro', 'pizzeria', 'sushi', 'diner', 'fast_food',
                            # Descriptive modifiers
                            'fancy', 'upscale', 'casual', 'dark', 'bright', 'modern', 'old', 'vintage']
            
            found_words = [word for word in words if word in location_words]
            
            if found_words:
                # Smart combination: cuisine + restaurant, descriptors + locations
                cuisine_types = ['italian', 'chinese', 'mexican', 'thai', 'indian', 'french', 'japanese',
                               'korean', 'vietnamese', 'greek', 'middle_eastern', 'mediterranean']
                descriptors = ['fancy', 'upscale', 'casual', 'dark', 'bright', 'modern', 'old', 'vintage']
                
                cuisines = [w for w in found_words if w in cuisine_types]
                descriptive = [w for w in found_words if w in descriptors]
                locations = [w for w in found_words if w not in cuisine_types and w not in descriptors]
                
                # Build intelligent name
                name_parts = []
                if descriptive and cuisines:
                    name_parts = [descriptive[0], cuisines[0], 'restaurant']
                elif cuisines:
                    name_parts = [cuisines[0], 'restaurant']
                elif descriptive and locations:
                    name_parts = [descriptive[0]] + locations[:1]
                else:
                    name_parts = found_words[:2]
                
                return '_'.join(name_parts)
            else:
                return "generic_location"
    
    def generate_background_image(self, speech_text: str, min_interval: float = 15, time_since_last: float = 0) -> Optional[tuple]:
        """Generate background image from speech text"""
        try:
            # First check if this speech contains location context
            if not self.detect_location_context(speech_text):
                print(f"🚫 No location context detected in: '{speech_text}' - skipping image generation")
                return None
            
            print(f"📍 Location detected - checking library for: '{speech_text}'")
            
            # Extract environment name for library check
            environment_name = self._extract_environment_name(speech_text)
            filename = f"{environment_name}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            # Check if environment already exists in library
            if os.path.exists(filepath):
                print(f"📚 Found existing environment: {environment_name}")
                print(f"♻️ Reusing: {filepath}")
                return (filepath, True)  # Return tuple: (path, was_reused)
            
            # Check rate limiting for new generation
            if time_since_last < min_interval:
                print(f"🕐 Rate limited - waiting {min_interval - time_since_last:.1f}s before generating new image")
                return None
            
            print(f"🎨 Generating new environment: {environment_name}")
            
            # Enhance the prompt
            enhanced_prompt = self.enhance_prompt_for_background(speech_text)
            
            # Generate image - use faster settings for live performance
            if self.fast_mode:
                # DALL-E 2: Much faster, good enough quality for live shows
                response = self.client.images.generate(
                    model="dall-e-2",
                    prompt=enhanced_prompt,
                    size="1024x1024",  # DALL-E 2 doesn't support wide format
                    n=1
                )
            else:
                # DALL-E 3: Higher quality but slower
                response = self.client.images.generate(
                    model="dall-e-3",
                    prompt=enhanced_prompt,
                    size="1792x1024",  # Wide format for theater backdrop
                    quality="standard",
                    n=1
                )
            
            # Download and save image
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                # Save image (environment_name and filepath already determined above)
                image = Image.open(io.BytesIO(image_response.content))
                image.save(filepath)
                
                print(f"📚 Environment saved to library: {filepath}")
                return (filepath, False)  # Return tuple: (path, was_reused=False for new generation)
            else:
                print("Failed to download generated image")
                return None
                
        except Exception as e:
            print(f"Error generating image: {e}")
            return None