import os
import json

# Define our paths
DATA_DIR = "./data"
FONT_FILE = "./fonts/NanumGothic-Regular.ttf"

def check_setup():
    print("--- 🧠 Brain Checkup ---")
    
    # 1. Check for Fonts
    if os.path.exists(FONT_FILE):
        print(f"✅ Font found: {FONT_FILE}")
    else:
        print("❌ Font NOT found. Check the spelling in the /fonts folder.")

    # 2. Check for JSON data
    print("\n--- 📁 Data Files Found ---")
    data_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    
    if not data_files:
        print("❌ No JSON files found in /data.")
    else:
        for file_name in data_files:
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # This assumes your JSON is a list or dict
                item_count = len(data) 
                print(f"✅ {file_name}: Loaded {item_count} items successfully.")

if __name__ == "__main__":
    check_setup()