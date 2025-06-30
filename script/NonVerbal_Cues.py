import pandas as pd
import json
import re

csv_path = "Dataset Preparation & Setup/script/cue_metadata_master_final_PJV.csv"
df = pd.read_csv(csv_path)
df.columns = [col.strip() for col in df.columns]

json_path = "Dataset Preparation & Setup/Metadata/Non_verbal_cues_extended.json"
with open(json_path, 'r') as f:
    non_verbal_cues = json.load(f)

def parse_emotion_alignment(emotion_str):
    if pd.isna(emotion_str):
        return []
    return [e.strip() for e in emotion_str.split(',')]

def normalize_cue_name(name):
    return re.sub(r'[_\-]', '', name).lower()

json_base_map = {}
for key in non_verbal_cues.keys():
    base_name_match = re.match(r"(.+?)(_[^_]+)?$", key)
    base_name = base_name_match.group(1) if base_name_match else key
    base_name_norm = normalize_cue_name(base_name)
    json_base_map.setdefault(base_name_norm, []).append(key)

for idx, row in df.iterrows():
    cue_id = row['Cue ID']
    cue_id_norm = normalize_cue_name(cue_id)
    
    if cue_id_norm not in json_base_map:
        print(f"Warning: Cue ID '{cue_id}' (normalized '{cue_id_norm}') not found in JSON keys")
        continue
    
    matching_keys = json_base_map[cue_id_norm]
    emotion_list = parse_emotion_alignment(row['Emotion Alignment'])
    usage_context = row.get("Usage Context", "") or ""
    insertion_timing = row.get("Insertion Timing", "") or ""
    
    for key in matching_keys:
        non_verbal_cues[key]["usage_context"] = usage_context
        non_verbal_cues[key]["insertion_timing"] = insertion_timing
        non_verbal_cues[key]["emotion_alignment"] = emotion_list
        # DEBUG print to verify update
        print(f"Updated key: {key}")
        print(json.dumps(non_verbal_cues[key], indent=2))

with open("non_verbal_cues_updated.json", "w") as f_out:
    json.dump(non_verbal_cues, f_out, indent=4)

print("non_verbal_cues_extended.json updated successfully!")
