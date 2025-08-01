#!/usr/bin/env python3

import os
import glob
import shutil
from dotenv import load_dotenv
from image_generator import AIImageGenerator

def show_library():
    """Show all environments in the library"""
    images_dir = "generated_images"
    files = sorted([f for f in os.listdir(images_dir) if f.endswith('.png')])
    
    print("📚 Complete Environment Library")
    print("=" * 40)
    
    if not files:
        print("No environments in library yet.")
        return
    
    for i, filename in enumerate(files, 1):
        env_name = filename.replace('.png', '').replace('_', ' ')
        size = os.path.getsize(os.path.join(images_dir, filename)) // 1024
        print(f"{i:2d}. {env_name} ({size}KB)")

def clean_old_files():
    """Convert old timestamp files to proper environment names"""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Need OpenAI API key to rename files")
        return
    
    generator = AIImageGenerator(api_key, fast_mode=True)
    images_dir = "generated_images"
    
    # Find old timestamp files
    old_files = glob.glob(os.path.join(images_dir, "background_*.png"))
    
    if not old_files:
        print("No old timestamp files found.")
        return
    
    print(f"Found {len(old_files)} old timestamp files to rename...")
    
    for old_file in old_files:
        try:
            # Try to extract environment from filename or ask user
            old_name = os.path.basename(old_file)
            print(f"\nRenaming: {old_name}")
            
            # Ask user what environment this represents
            description = input("What environment does this represent? (e.g., 'beach day', 'coffee shop'): ")
            
            if description.strip():
                # Clean up the description
                new_name = description.lower().replace(' ', '_')
                new_name = ''.join(c for c in new_name if c.isalnum() or c == '_')
                new_path = os.path.join(images_dir, f"{new_name}.png")
                
                # Check if new name already exists
                if os.path.exists(new_path):
                    print(f"Environment '{new_name}' already exists. Skipping.")
                    continue
                
                # Rename the file
                shutil.move(old_file, new_path)
                print(f"✅ Renamed to: {new_name}.png")
            else:
                print("Skipped.")
                
        except Exception as e:
            print(f"Error renaming {old_file}: {e}")

def main():
    """Main library management interface"""
    print("🎭 Improv AI - Environment Library Manager")
    print("=" * 45)
    
    while True:
        print("\nOptions:")
        print("1. Show library")
        print("2. Clean old timestamp files")
        print("3. Exit")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            show_library()
        elif choice == "2":
            clean_old_files()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()