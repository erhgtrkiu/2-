import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def parse_and_print(filename):
    print(f"=== Parsing {filename} ===")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        content = data.get('content', '')
        print(content)
    except Exception as e:
        print("Error:", e)

# Parse line 2665 and 2670
parse_and_print('scratch/raw_line_2665.txt')
parse_and_print('scratch/raw_line_2670.txt')
