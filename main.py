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

def save_prompt_to_file(book, day, content):
    # Ensure we are saving inside the project folder
    base_path = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(base_path, "outputs", book)
    
    os.makedirs(export_dir, exist_ok=True)
    
    # Using a timestamp to prevent overwriting if you run it multiple times
    from datetime import datetime
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"DAY_{day.zfill(2)}_{timestamp}.txt"
    file_path = os.path.join(export_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ FILE SAVED TO: {file_path}")

def generate_prompt(words, grammar):
    word_str = ", ".join([f"{w['word']} ({w['korean']})" for w in words])
    
    prompt = (
        "### ROLE: SENIOR LINGUIST & TEST ARCHITECT\n"
        "### GOAL: Generate a high-rigor Korean Middle School level challenge.\n\n"
        "### INPUT DATA:\n"
        f"- Vocabulary: {word_str}\n"
        f"- Grammar: {grammar['rule_name']} ({grammar['korean_explanation']})\n\n"
        "### [STRICT RULES]:\n"
        "1. **Difficulty**: Match Middle School 'Naesin' (내신) exam rigor.\n"
        "2. **Morphology**: TRANSFORM target words (tense, voice, part of speech) "
        "to fit the grammar focus. NO non-words.\n"
        "3. **Context**: 2 target words per sentence (1 blank, 1 **bold** context).\n\n"
        "### OUTPUT FORMAT:\n"
        "Generate 10 questions followed by a BILINGUAL ANSWER KEY.\n"
        "The key must explain the grammatical transformation (tense/voice) in Korean.\n"
    )
    return prompt

if __name__ == "__main__":
    # Settings
    book = "eohwi_kkuet"
    day = "14"
    
    # Execution: Just run it once. For a second version, just run the script again!
    words, grammar = get_session_data(book, day)
    final_prompt = generate_prompt(words, grammar)
    
    # Save and Print
    save_prompt_to_file(book, day, final_prompt)
    print(f"\n--- GENERATED PROMPT ---\n{final_prompt}")