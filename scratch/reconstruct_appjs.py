import json
import os
import re

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'
original_path = r'C:\Users\m3615\samosbor_game\scratch\app_original.js'

with open(original_path, 'r', encoding='utf-8') as f:
    current_content = f.read()

print(f"Original content length: {len(current_content)} characters")

edits = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        tool_calls = data.get('tool_calls', [])
        
        for tc in tool_calls:
            name = tc.get('name')
            if name in ('replace_file_content', 'multi_replace_file_content', 'write_to_file'):
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: pass
                
                if isinstance(args, dict):
                    target = args.get('TargetFile', '')
                    if 'app.js' in target and not 'inspect_old_app.js' in target and not 'replace_textures_in_app.js' in target:
                        edits.append({
                            'step_index': step_index,
                            'tool': name,
                            'args': args
                        })

print(f"Found {len(edits)} edits to app.js")

for edit in edits:
    step = edit['step_index']
    tool = edit['tool']
    args = edit['args']
    
    if tool == 'write_to_file':
        # Let's check if it overwrites the entire file or is a specific write
        code = args.get('CodeContent', '')
        overwrite = args.get('Overwrite', False)
        # In steps 21, 75, 95, etc. they might be writing app.js, let's see:
        # If the code length is very large or if it's the beginning of the file:
        print(f"Step {step}: write_to_file, code length = {len(code)}, overwrite = {overwrite}")
        if len(code) > 200000: # large write
            current_content = code
            print(f"  Overwrote content with new code of length {len(code)}")
        else:
            # Check if this is indeed a full overwrite or a snippet
            if overwrite:
                print(f"  WARNING: small write_to_file with overwrite=True at step {step}! Length = {len(code)}")
                # Let's see what it is
                print(f"  Code sample: {code[:150]}...")
                # If it's a small script, don't overwrite current_content of the game!
                # Wait, let's inspect if it was a mistake or not
    
    elif tool == 'replace_file_content':
        target = args.get('TargetContent', '')
        replacement = args.get('ReplacementContent', '')
        if not target:
            print(f"Step {step}: replace_file_content has empty TargetContent!")
            continue
            
        # Try to find target in current_content
        occurrences = current_content.count(target)
        if occurrences == 0:
            print(f"Step {step}: replace_file_content target not found!")
            # Normalize line endings and try again
            norm_target = target.replace('\r\n', '\n')
            norm_content = current_content.replace('\r\n', '\n')
            if norm_content.count(norm_target) == 1:
                print(f"  Fixed target by normalizing line endings.")
                norm_content = norm_content.replace(norm_target, replacement.replace('\r\n', '\n'))
                current_content = norm_content
            else:
                print(f"  FAILED to find target: {repr(target[:100])}...")
        elif occurrences > 1:
            print(f"Step {step}: replace_file_content target has {occurrences} occurrences! Ambiguous.")
        else:
            current_content = current_content.replace(target, replacement)
            print(f"Step {step}: replace_file_content applied successfully.")
            
    elif tool == 'multi_replace_file_content':
        chunks = args.get('ReplacementChunks', [])
        print(f"Step {step}: multi_replace_file_content with {len(chunks)} chunks.")
        # Apply chunks
        for idx, chunk in enumerate(chunks):
            target = chunk.get('TargetContent', '')
            replacement = chunk.get('ReplacementContent', '')
            occurrences = current_content.count(target)
            if occurrences == 0:
                # Try normalized
                norm_target = target.replace('\r\n', '\n')
                norm_content = current_content.replace('\r\n', '\n')
                if norm_content.count(norm_target) == 1:
                    norm_content = norm_content.replace(norm_target, replacement.replace('\r\n', '\n'))
                    current_content = norm_content
                    print(f"  Chunk {idx} applied with normalization.")
                else:
                    print(f"  Chunk {idx} target not found!")
            elif occurrences > 1:
                print(f"  Chunk {idx} target has {occurrences} occurrences! Ambiguous.")
            else:
                current_content = current_content.replace(target, replacement)
                print(f"  Chunk {idx} applied successfully.")

# Save the reconstructed file
reconstructed_path = r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js'
with open(reconstructed_path, 'w', encoding='utf-8') as f:
    f.write(current_content)

print(f"Reconstructed file written to {reconstructed_path}, length = {len(current_content)} characters")
