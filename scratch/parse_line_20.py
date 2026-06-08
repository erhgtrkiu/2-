import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('scratch/raw_line_20.txt', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("KEYS:", data.keys())
    tcalls = data.get('tool_calls', [])
    print("Num tool calls:", len(tcalls))
    for idx, tc in enumerate(tcalls):
        print(f"Tool {idx}: name={tc.get('name')}")
        args = tc.get('args', {})
        print("  keys in args:", list(args.keys()))
        for k, v in args.items():
            s = str(v)
            print(f"  {k}: {s[:300]} ... len={len(s)}")
except Exception as e:
    print("Error:", e)
