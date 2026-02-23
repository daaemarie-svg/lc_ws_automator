import os
import json

# --- 1. SETUP PATHS ---
DATA_ROOT = "./data"
OUTPUT_ROOT = "./data/standardized"

# --- 2. THE WASHER FUNCTIONS ---
def wash_single_file(in_path, file_name, out_path, category):
    """Processes one vocabulary JSON list into the standard format."""
    with open(os.path.join(in_path, file_name), 'r', encoding='utf-8') as f:
        dirty_data = json.load(f)
    
    clean_data = []
    for i, entry in enumerate(dirty_data):
        # We only keep what we need for the 'Golden Nuggets'
        clean_data.append({
            "id": f"{category[:3].upper()}-{i+1:03}",
            "word": entry.get("word"),
            "korean": entry.get("meaning"),
            "level": category
        })
        
    with open(os.path.join(out_path, file_name), 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=4)

def wash_grammar_file(in_path, out_path):
    """Special washer for the dictionary-style grammar_bank.json"""
    file_name = "grammar_bank.json"
    full_in_path = os.path.join(in_path, file_name)
    
    if not os.path.exists(full_in_path):
        return

    with open(full_in_path, 'r', encoding='utf-8') as f:
        dirty_grammar = json.load(f)
    
    clean_grammar = []
    for rule_key, details in dirty_grammar.items():
        clean_grammar.append({
            "id": f"GRAM-{rule_key.upper()[:5]}",
            "rule_name": details.get("en"),
            "korean_explanation": details.get("kr"),
            "example_sentence": details.get("example_en"),
            "level": details.get("level")
        })
        
    with open(os.path.join(out_path, "grammar_standardized.json"), 'w', encoding='utf-8') as f:
        json.dump(clean_grammar, f, ensure_ascii=False, indent=4)

# --- 3. THE MASTER CONTROLLER ---
def wash_all_folders():
    """Loops through the data directory to find and clean every folder."""
    if not os.path.exists(DATA_ROOT):
        print(f"Error: {DATA_ROOT} folder not found!")
        return

    print("📄 Processing grammar_bank.json...")
    wash_grammar_file(DATA_ROOT, OUTPUT_ROOT)

    

    for folder_name in os.listdir(DATA_ROOT):
        folder_path = os.path.join(DATA_ROOT, folder_name)
        
        # Skip the output folder and the grammar file (it's a different shape)
        if folder_name == "standardized" or not os.path.isdir(folder_path):
            continue
            
        print(f"Processing folder: {folder_name}...")
        
        # Create matching subfolders in standardized (e.g., standardized/wm_basic)
        out_folder = os.path.join(OUTPUT_ROOT, folder_name)
        os.makedirs(out_folder, exist_ok=True)
        
        # Look for JSON actors in the room
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                wash_single_file(folder_path, file_name, out_folder, folder_name)

# --- 4. EXECUTION ---
if __name__ == "__main__":
    wash_all_folders()
    print("✨ All folders standardized and moved to /data/standardized!")