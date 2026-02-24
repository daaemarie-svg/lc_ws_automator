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
def get_session_data(folder_name, day_number, count=10):
    """Picks the actors for our worksheet."""
    vocab_folder = os.path.join(DATA_DIR, folder_name)
    grammar_file = os.path.join(DATA_DIR, "grammar_standardized.json")

    # 1. Grab a specific vocab file from the folder
    
    prefix = "UNIT" if folder_name == "eohwi_kkuet" else "DAY"
    target_file = f"{prefix}_{day_number.zfill(2)}.json"

    
    with open(os.path.join(vocab_folder, target_file), 'r', encoding='utf-8') as f:
        vocab_list = json.load(f)
    
    with open(grammar_file, 'r', encoding='utf-8') as f:
        grammar_list = json.load(f)

    # 2. Select 10 random words and 1 random grammar rule
    selected_words = random.sample(vocab_list, min(count, len(vocab_list)))
    selected_grammar = random.choice(grammar_list)

    return selected_words, selected_grammar

def generate_prompt(words, grammar):
    word_str = ", ".join([f"{w['word']} ({w['korean']})" for w in words])
    
    # Each line is its own string; Python joins them because of the ( )
    prompt = (
        "### ROLE: SENIOR LINGUIST & TEST ARCHITECT\n"
        "### GOAL: Generate a high-rigor linguistic challenge.\n\n"
        "### INPUT DATA:\n"
        f"- Target Vocabulary: {word_str}\n"
        f"- Target Grammar: {grammar['rule_name']} ({grammar['korean_explanation']})\n\n"
        "### [STRICT RULES]:\n"
        "1. **Contextual Integration**: Use 2 target words per sentence: "
        "one blank (_______) and one **bolded** context word.\n"
        "2. **Bilingual Flow**: English sentence followed by Korean translation.\n"
        "3. **Morphological Rigor**: Transform tenses/parts of speech to match "
        "grammar. No non-existent words.\n"
        "4. **Formatting**: **Bold** all non-blank target words.\n\n"
        "### OUTPUT FORMAT:\n"
        "Q1. [English Sentence]\n[Korean Translation]\nA) B) C) D)\n"
    )
    return prompt

def save_prompt_to_file(folder_name, day_number, version, content):
    # 1. Create the path: outputs/[book_name]/
    export_dir = os.path.join("outputs", folder_name)
    os.makedirs(export_dir, exist_ok=True)
    
    # 2. Name the file: UNIT_13_Version_A.txt
    filename = f"DAY_{day_number.zfill(2)}_Version_{version}.txt"
    file_path = os.path.join(export_dir, filename)
    
    # 3. Save the content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Saved to: {file_path}")

if __name__ == "__main__":
    # We want two distinct versions
    versions = ["A", "B"]
    
    for v in versions:
        print(f"\n--- 📝 GENERATING VERSION {v} ---")
        
        # 1. Get new random ingredients for this version
        words, grammar = get_session_data("eohwi_kkuet", "13")
        
        # 2. Build the prompt with those specific ingredients
        final_prompt = generate_prompt(words, grammar)
        
        # 3. Output to terminal
        print(final_prompt)
        print("-" * 30)