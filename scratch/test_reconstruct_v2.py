import json
import os

transcript_path = r'C:\Users\m3615\.gemini\antigravity\brain\68589a5c-391d-4fb4-bd7d-f6ad216b12ae\.system_generated\logs\transcript.jsonl'
original_path = r'C:\Users\m3615\samosbor_game\scratch\app_original.js'

with open(original_path, 'r', encoding='utf-8') as f:
    current_content = f.read()

def clean_val(val):
    if not isinstance(val, str):
        return val
    # If it's a JSON-stringified string (starts and ends with quotes)
    if val.startswith('"') and val.endswith('"') and len(val) >= 2:
        try:
            return json.loads(val, strict=False)
        except Exception:
            pass
    # Also resolve escaped newlines if present
    if '\\n' in val or '\\r' in val or '\\t' in val:
        try:
            return json.loads(f'"{val}"', strict=False)
        except Exception:
            return val.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')
    return val

edits = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line, strict=False)
        except Exception:
            continue
        
        step_index = data.get('step_index')
        tool_calls = data.get('tool_calls', [])
        
        for tc in tool_calls:
            name = tc.get('name')
            if name in ('replace_file_content', 'multi_replace_file_content', 'write_to_file'):
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args, strict=False)
                    except: pass
                
                if isinstance(args, dict):
                    target = args.get('TargetFile', '')
                    target = clean_val(target)
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
        code = clean_val(args.get('CodeContent', ''))
        overwrite = args.get('Overwrite', False)
        if isinstance(overwrite, str):
            overwrite = (overwrite.lower() == 'true')
            
        print(f"Step {step}: write_to_file, code length = {len(code)}, overwrite = {overwrite}")
        if len(code) > 200000:
            current_content = code
            print(f"  Overwrote content with new code of length {len(code)}")
        else:
            if overwrite:
                print(f"  WARNING: small write_to_file with overwrite=True at step {step}! Length = {len(code)}")
                print(f"  Code sample: {repr(code[:150])}...")
                if len(code) < 10000:
                    print("  Skipping this write_to_file to avoid destroying the codebase.")
                else:
                    current_content = code
                    
    elif tool == 'replace_file_content':
        target = clean_val(args.get('TargetContent', ''))
        replacement = clean_val(args.get('ReplacementContent', ''))
        if not target:
            continue
            
        occurrences = current_content.count(target)
        if occurrences == 0:
            norm_target = target.replace('\r\n', '\n')
            norm_content = current_content.replace('\r\n', '\n')
            if norm_content.count(norm_target) == 1:
                current_content = norm_content.replace(norm_target, replacement.replace('\r\n', '\n'))
                print(f"Step {step}: replace_file_content applied with line ending normalization.")
            else:
                print(f"Step {step}: replace_file_content target not found! Length = {len(target)}")
                print(f"  Target sample: {repr(target[:100])}...")
        elif occurrences > 1:
            print(f"Step {step}: replace_file_content target has {occurrences} occurrences! Ambiguous.")
        else:
            current_content = current_content.replace(target, replacement)
            print(f"Step {step}: replace_file_content applied successfully.")
            
    elif tool == 'multi_replace_file_content':
        chunks_raw = args.get('ReplacementChunks', [])
        if isinstance(chunks_raw, str):
            try:
                # Fix raw string by escaping newlines and tabs
                fixed_raw = chunks_raw.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                chunks = json.loads(fixed_raw, strict=False)
            except Exception as e:
                print(f"Step {step}: multi_replace_file_content chunks parse error: {e}")
                continue
        else:
            chunks = chunks_raw
            
        print(f"Step {step}: multi_replace_file_content with {len(chunks)} chunks.")
        for idx, chunk in enumerate(chunks):
            target = clean_val(chunk.get('TargetContent', ''))
            replacement = clean_val(chunk.get('ReplacementContent', ''))
            
            occurrences = current_content.count(target)
            if occurrences == 0:
                norm_target = target.replace('\r\n', '\n')
                norm_content = current_content.replace('\r\n', '\n')
                if norm_content.count(norm_target) == 1:
                    current_content = norm_content.replace(norm_target, replacement.replace('\r\n', '\n'))
                    print(f"  Chunk {idx} applied with line ending normalization.")
                else:
                    print(f"  Chunk {idx} target not found! Length = {len(target)}")
                    print(f"    Target sample: {repr(target[:100])}...")
            elif occurrences > 1:
                print(f"  Chunk {idx} target has {occurrences} occurrences! Ambiguous.")
            else:
                current_content = current_content.replace(target, replacement)
                print(f"  Chunk {idx} applied successfully.")

reconstructed_path = r'C:\Users\m3615\samosbor_game\scratch\app_reconstructed.js'
with open(reconstructed_path, 'w', encoding='utf-8') as f:
    f.write(current_content)

print(f"Reconstructed file written to {reconstructed_path}, length = {len(current_content)} characters")
