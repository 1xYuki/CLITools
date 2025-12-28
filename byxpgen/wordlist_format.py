import os

BASE_DIR = r"C:\Users\LEPUser\Documents\GitHub\CLITools"
INPUT_FILE = os.path.join(BASE_DIR, "wordlist.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "wordlist_clean.py")

print("Working directory:", BASE_DIR)
print("Reading from:", INPUT_FILE)

words = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # EFF format: number + whitespace + word
        word = line.split()[-1]
        words.append(word)

print(f"Processed {len(words)} words")

if not words:
    raise RuntimeError("No words were parsed — check input file contents.")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("# Auto-generated from EFF wordlist\n")
    f.write("WORDLIST = [\n")
    
    # Write 10 words per line
    for i in range(0, len(words), 10):
        chunk = words[i:i+10]
        formatted_chunk = ", ".join(f"'{word}'" for word in chunk)
        f.write(f"    {formatted_chunk},\n")
    
    f.write("]\n")

print("Wrote cleaned wordlist to:", OUTPUT_FILE)