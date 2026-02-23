import os
import json
import random

# Define our paths
DATA_DIR = "./data/standardized"
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

    #3.  'Brain' logic 
def get_session_data(folder_name, count=10):
    """Picks the actors for our worksheet."""
    vocab_folder = os.path.join(DATA_DIR, folder_name)
    grammar_file = os.path.join(DATA_DIR, "grammar_standardized.json")

    # 1. Grab a random vocab file from the folder (e.g., DAY_01.json)
    all_files = [f for f in os.listdir(vocab_folder) if f.endswith('.json')]
    target_file = random.choice(all_files)
    
    with open(os.path.join(vocab_folder, target_file), 'r', encoding='utf-8') as f:
        vocab_list = json.load(f)
    
    with open(grammar_file, 'r', encoding='utf-8') as f:
        grammar_list = json.load(f)

    # 2. Select 10 random words and 1 random grammar rule
    selected_words = random.sample(vocab_list, min(count, len(vocab_list)))
    selected_grammar = random.choice(grammar_list)

    return selected_words, selected_grammar

if __name__ == "__main__":
    check_setup()

    # --- 🎲 Test the Selector ---
    print("\n--- 🎲 Testing Random Selection ---")
    # Let's try picking from 'wm_basic'
    words, grammar = get_session_data("wm_basic")
    
    print(f"Target Grammar: {grammar['rule_name']}")
    print(f"First Word Picked: {words[0]['word']} ({words[0]['korean']})")