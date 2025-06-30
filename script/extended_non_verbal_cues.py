# import os
# import json
# import librosa
# import numpy as np
# from collections import Counter
# from tqdm import tqdm

# # Paths
# BASE_DIR = "Dataset Preparation & Setup/project_voltron_dataset"
# SPEAKER_DIRS = ["female/nonverbal_cues", "male/nonverbal_cues"]
# OUTPUT_JSON = "non_verbal_metadata.json"

# def analyze_audio(audio_path):
#     y, sr = librosa.load(audio_path, sr=24000)
#     duration = librosa.get_duration(y=y, sr=sr)

#     amplitude_min = float(np.min(y))
#     amplitude_max = float(np.max(y))

#     hop_length = 512
#     frame_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length).flatten()
#     time_stamps = librosa.frames_to_time(np.arange(len(frame_energy)), sr=sr, hop_length=hop_length)
#     frame_energy /= frame_energy.max() + 1e-6

#     peak_frame = np.argmax(frame_energy)
#     peak_time = time_stamps[peak_frame]
#     peak_percent = peak_time / duration
#     if peak_percent < 0.2:
#         prosody_hint = "sharp attack at start"
#     elif peak_percent < 0.5:
#         prosody_hint = "crescendo around 30-40% of duration"
#     elif peak_percent < 0.75:
#         prosody_hint = "crescendo around 60% of duration"
#     else:
#         prosody_hint = "crescendo around 75% of duration"
#     if frame_energy[-1] < 0.3 * frame_energy.max():
#         prosody_hint += ", fade out after 70%"

#     try:
#         pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#         pitches = pitches[magnitudes > np.median(magnitudes)]
#         pitches = pitches[pitches > 0]
#         if len(pitches) > 0:
#             f0_mean = np.mean(pitches)
#             pitch_jitter_cents = np.std(1200 * np.log2(pitches / f0_mean))
#         else:
#             pitch_jitter_cents = 0.0
#     except:
#         pitch_jitter_cents = 0.0

#     time_jitter_pct = np.std(frame_energy) * 100 if len(frame_energy) > 1 else 0.0

#     return {
#         "prosody_hint": prosody_hint,
#         "default_offsets": {"start": 0.0, "end": round(duration, 2)},
#         "duration_range": {"min": 0.0, "max": round(duration, 2)},
#         "amplitude_range": {"min": round(amplitude_min, 3), "max": round(amplitude_max, 3)},
#         "variation_params": {
#             "pitch_jitter_cents": round(pitch_jitter_cents, 2),
#             "time_jitter_pct": round(time_jitter_pct, 2)
#         }
#     }

# # Step 1: Count total files per category across speakers
# category_counter = Counter()
# category_files = {}

# for speaker in SPEAKER_DIRS:
#     speaker_path = os.path.join(BASE_DIR, speaker)
#     for category in os.listdir(speaker_path):
#         category_path = os.path.join(speaker_path, category)
#         if os.path.isdir(category_path):
#             wavs = [f for f in os.listdir(category_path) if f.endswith('.wav')]
#             category_counter[category] += len(wavs)
#             for wav in wavs:
#                 category_files[os.path.join(speaker, category, wav)] = category

# total_files = sum(category_counter.values())
# probability_weights = {cat: round(count / total_files, 4) for cat, count in category_counter.items()}

# # Step 2: Generate metadata
# nonverbal_metadata = {}

# for file_rel_path, category in tqdm(category_files.items(), desc="Processing files"):
#     file_path = os.path.join(BASE_DIR, file_rel_path)
#     analysis = analyze_audio(file_path)

#     key = category.lower().replace(" ", "_")
#     speaker = file_rel_path.split("/")[0].lower()

#     if key not in nonverbal_metadata:
#         nonverbal_metadata[key] = {
#             "description": f"Sound of {category}.",
#             "probability_weight": probability_weights.get(category, 0),
#             "examples": []
#         }

#     nonverbal_metadata[key]["examples"].append({
#         "file_path": file_rel_path,
#         "speaker": speaker,
#         "prosody_hint": analysis["prosody_hint"],
#         "default_offsets": analysis["default_offsets"],
#         "duration_range": analysis["duration_range"],
#         "amplitude_range": analysis["amplitude_range"],
#         "variation_params": analysis["variation_params"]
#     })

# # Step 3: Save JSON
# with open(OUTPUT_JSON, 'w') as f:
#     json.dump(nonverbal_metadata, f, indent=4)

# print(f"✅ Non-verbal metadata saved to {OUTPUT_JSON}")


# import os
# import json
# import librosa
# import numpy as np
# from collections import Counter
# from tqdm import tqdm

# # Paths
# BASE_DIR = "Dataset Preparation & Setup/project_voltron_dataset"
# SPEAKER_DIRS = ["female/nonverbal_cues", "male/nonverbal_cues"]
# OUTPUT_JSON = "Dataset Preparation & Setup/non_verbal_metadata.json"

# def analyze_audio(audio_path):
#     y, sr = librosa.load(audio_path, sr=24000)
#     duration = float(librosa.get_duration(y=y, sr=sr))

#     amplitude_min = float(np.min(y))
#     amplitude_max = float(np.max(y))

#     hop_length = 512
#     frame_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length).flatten()
#     time_stamps = librosa.frames_to_time(np.arange(len(frame_energy)), sr=sr, hop_length=hop_length)
#     frame_energy = frame_energy / (np.max(frame_energy) + 1e-6)

#     peak_frame = int(np.argmax(frame_energy))
#     peak_time = float(time_stamps[peak_frame])
#     peak_percent = peak_time / duration

#     if peak_percent < 0.2:
#         prosody_hint = "sharp attack at start"
#     elif peak_percent < 0.5:
#         prosody_hint = "crescendo around 30-40% of duration"
#     elif peak_percent < 0.75:
#         prosody_hint = "crescendo around 60% of duration"
#     else:
#         prosody_hint = "crescendo around 75% of duration"

#     if frame_energy[-1] < 0.3 * np.max(frame_energy):
#         prosody_hint += ", fade out after 70%"

#     try:
#         pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#         pitches = pitches[magnitudes > np.median(magnitudes)]
#         pitches = pitches[pitches > 0]
#         if len(pitches) > 0:
#             f0_mean = float(np.mean(pitches))
#             pitch_jitter_cents = float(np.std(1200 * np.log2(pitches / f0_mean)))
#         else:
#             pitch_jitter_cents = 0.0
#     except:
#         pitch_jitter_cents = 0.0

#     time_jitter_pct = float(np.std(frame_energy) * 100) if len(frame_energy) > 1 else 0.0

#     return {
#         "prosody_hint": prosody_hint,
#         "default_offsets": {"start": 0.0, "end": round(duration, 2)},
#         "duration_range": {"min": 0.0, "max": round(duration, 2)},
#         "amplitude_range": {"min": round(amplitude_min, 3), "max": round(amplitude_max, 3)},
#         "variation_params": {
#             "pitch_jitter_cents": round(pitch_jitter_cents, 2),
#             "time_jitter_pct": round(time_jitter_pct, 2)
#         }
#     }

# # Step 1: Count total files per category across speakers
# category_counter = Counter()
# category_files = {}

# for speaker in SPEAKER_DIRS:
#     speaker_path = os.path.join(BASE_DIR, speaker)
#     for category in os.listdir(speaker_path):
#         category_path = os.path.join(speaker_path, category)
#         if os.path.isdir(category_path):
#             wavs = [f for f in os.listdir(category_path) if f.endswith('.wav')]
#             category_counter[category] += len(wavs)
#             for wav in wavs:
#                 category_files[os.path.join(speaker, category, wav)] = category

# total_files = sum(category_counter.values())
# probability_weights = {cat: round(count / total_files, 4) for cat, count in category_counter.items()}

# # Step 2: Generate metadata
# nonverbal_metadata = {}

# for file_rel_path, category in tqdm(category_files.items(), desc="Processing files"):
#     file_path = os.path.join(BASE_DIR, file_rel_path)
#     analysis = analyze_audio(file_path)

#     key = category.lower().replace(" ", "_")
#     speaker = file_rel_path.split("/")[0].lower()

#     if key not in nonverbal_metadata:
#         nonverbal_metadata[key] = {
#             "description": f"Sound of {category}.",
#             "probability_weight": float(probability_weights.get(category, 0)),
#             "examples": []
#         }

#     nonverbal_metadata[key]["examples"].append({
#         "file_path": file_rel_path,
#         "speaker": speaker,
#         "prosody_hint": analysis["prosody_hint"],
#         "default_offsets": analysis["default_offsets"],
#         "duration_range": analysis["duration_range"],
#         "amplitude_range": analysis["amplitude_range"],
#         "variation_params": analysis["variation_params"]
#     })

# # Step 3: Save JSON
# with open(OUTPUT_JSON, 'w') as f:
#     json.dump(nonverbal_metadata, f, indent=4)

# print(f"✅ Non-verbal metadata saved to {OUTPUT_JSON}")

# import os
# import json
# import librosa
# import numpy as np
# from collections import Counter
# from tqdm import tqdm

# # Paths
# BASE_DIR = "Dataset Preparation & Setup/project_voltron_dataset"
# SPEAKER_DIRS = ["female/nonverbal_cues", "male/nonverbal_cues"]
# OUTPUT_JSON_FEMALE = "Dataset Preparation & Setup/non_verbal_metadata_female.json"
# OUTPUT_JSON_MALE = "Dataset Preparation & Setup/non_verbal_metadata_male.json"

# def analyze_audio(audio_path):
#     y, sr = librosa.load(audio_path, sr=24000)
#     duration = float(librosa.get_duration(y=y, sr=sr))

#     amplitude_min = float(np.min(y))
#     amplitude_max = float(np.max(y))

#     hop_length = 512
#     frame_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length).flatten()
#     time_stamps = librosa.frames_to_time(np.arange(len(frame_energy)), sr=sr, hop_length=hop_length)
#     frame_energy = frame_energy / (np.max(frame_energy) + 1e-6)

#     peak_frame = int(np.argmax(frame_energy))
#     peak_time = float(time_stamps[peak_frame])
#     peak_percent = peak_time / duration

#     if peak_percent < 0.2:
#         prosody_hint = "sharp attack at start"
#     elif peak_percent < 0.5:
#         prosody_hint = "crescendo around 30-40% of duration"
#     elif peak_percent < 0.75:
#         prosody_hint = "crescendo around 60% of duration"
#     else:
#         prosody_hint = "crescendo around 75% of duration"

#     if frame_energy[-1] < 0.3 * np.max(frame_energy):
#         prosody_hint += ", fade out after 70%"

#     try:
#         pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#         pitches = pitches[magnitudes > np.median(magnitudes)]
#         pitches = pitches[pitches > 0]
#         if len(pitches) > 0:
#             f0_mean = float(np.mean(pitches))
#             pitch_jitter_cents = float(np.std(1200 * np.log2(pitches / f0_mean)))
#         else:
#             pitch_jitter_cents = 0.0
#     except:
#         pitch_jitter_cents = 0.0

#     time_jitter_pct = float(np.std(frame_energy) * 100) if len(frame_energy) > 1 else 0.0

#     return {
#         "prosody_hint": prosody_hint,
#         "default_offsets": {"start": 0.0, "end": round(duration, 2)},
#         "duration_range": {"min": 0.0, "max": round(duration, 2)},
#         "amplitude_range": {"min": round(amplitude_min, 3), "max": round(amplitude_max, 3)},
#         "variation_params": {
#             "pitch_jitter_cents": round(pitch_jitter_cents, 2),
#             "time_jitter_pct": round(time_jitter_pct, 2)
#         }
#     }

# # Step 1: Count files per category for probability weights (shared across genders)
# category_counter = Counter()
# category_files = {}

# for speaker in SPEAKER_DIRS:
#     speaker_path = os.path.join(BASE_DIR, speaker)
#     for category in os.listdir(speaker_path):
#         category_path = os.path.join(speaker_path, category)
#         if os.path.isdir(category_path):
#             wavs = [f for f in os.listdir(category_path) if f.endswith('.wav')]
#             category_counter[category] += len(wavs)
#             for wav in wavs:
#                 category_files[os.path.join(speaker, category, wav)] = category

# total_files = sum(category_counter.values())
# probability_weights = {cat: round(count / total_files, 4) for cat, count in category_counter.items()}

# # Step 2: Generate metadata per gender
# nonverbal_metadata_female = {}
# nonverbal_metadata_male = {}

# for file_rel_path, category in tqdm(category_files.items(), desc="Processing files"):
#     file_path = os.path.join(BASE_DIR, file_rel_path)
#     analysis = analyze_audio(file_path)

#     key = category.lower().replace(" ", "_")
#     speaker = file_rel_path.split("/")[0].lower()

#     target_dict = nonverbal_metadata_female if speaker == "female" else nonverbal_metadata_male

#     if key not in target_dict:
#         target_dict[key] = {
#             "description": f"Sound of {category}.",
#             "probability_weight": float(probability_weights.get(category, 0)),
#             "examples": []
#         }

#     target_dict[key]["examples"].append({
#         "file_path": file_rel_path,
#         "speaker": speaker,
#         "prosody_hint": analysis["prosody_hint"],
#         "default_offsets": analysis["default_offsets"],
#         "duration_range": analysis["duration_range"],
#         "amplitude_range": analysis["amplitude_range"],
#         "variation_params": analysis["variation_params"]
#     })

# # Step 3: Save JSONs
# with open(OUTPUT_JSON_FEMALE, 'w') as f:
#     json.dump(nonverbal_metadata_female, f, indent=4)

# with open(OUTPUT_JSON_MALE, 'w') as f:
#     json.dump(nonverbal_metadata_male, f, indent=4)

# print(f"✅ Female metadata saved to {OUTPUT_JSON_FEMALE}")
# print(f"✅ Male metadata saved to {OUTPUT_JSON_MALE}")

import re
import os
import json
import librosa
import numpy as np
from collections import Counter
from tqdm import tqdm

# Paths
BASE_DIR = "Dataset Preparation & Setup/project_voltron_dataset"
SPEAKER_DIRS = ["female/nonverbal_cues", "male/nonverbal_cues"]
OUTPUT_JSON = "Dataset Preparation & Setup/Metadata/Non_verbal_cues_extended.json"

def split_camel_case(text):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)


def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=24000)
    duration = float(librosa.get_duration(y=y, sr=sr))

    amplitude_min = float(np.min(y))
    amplitude_max = float(np.max(y))

    hop_length = 512
    frame_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length).flatten()
    time_stamps = librosa.frames_to_time(np.arange(len(frame_energy)), sr=sr, hop_length=hop_length)
    frame_energy = frame_energy / (np.max(frame_energy) + 1e-6)

    peak_frame = int(np.argmax(frame_energy))
    peak_time = float(time_stamps[peak_frame])
    peak_percent = float(peak_time / duration) if duration > 0 else 0.0

    if peak_percent < 0.2:
        prosody_hint = "sharp attack at start"
    elif peak_percent < 0.5:
        prosody_hint = "crescendo around 30-40% of duration"
    elif peak_percent < 0.75:
        prosody_hint = "crescendo around 60% of duration"
    else:
        prosody_hint = "crescendo around 75% of duration"

    if frame_energy[-1] < 0.3 * np.max(frame_energy):
        prosody_hint += ", fade out after 70%"

    try:
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitches = pitches[magnitudes > np.median(magnitudes)]
        pitches = pitches[pitches > 0]
        if len(pitches) > 0:
            f0_mean = float(np.mean(pitches))
            pitch_jitter_cents = float(np.std(1200 * np.log2(pitches / f0_mean)))
        else:
            pitch_jitter_cents = 0.0
    except:
        pitch_jitter_cents = 0.0

    time_jitter_pct = float(np.std(frame_energy) * 100) if len(frame_energy) > 1 else 0.0

    return {
        "prosody_hint": prosody_hint,
        "default_offsets": {"start": 0.0, "end": round(duration, 2)},
        "duration_range": {"min": 0.0, "max": round(duration, 2)},
        "amplitude_range": {"min": round(amplitude_min, 3), "max": round(amplitude_max, 3)},
        "variation_params": {
            "pitch_jitter_cents": round(pitch_jitter_cents, 2),
            "time_jitter_pct": round(time_jitter_pct, 2)
        }
    }

# Step 1: Count total files per category across speakers
category_counter = Counter()
category_files = {}

for speaker in SPEAKER_DIRS:
    speaker_path = os.path.join(BASE_DIR, speaker)
    for category in os.listdir(speaker_path):
        category_path = os.path.join(speaker_path, category)
        if os.path.isdir(category_path):
            wavs = [f for f in os.listdir(category_path) if f.endswith('.wav')]
            category_counter[category] += len(wavs)
            for wav in wavs:
                category_files[os.path.join(speaker, category, wav)] = {
                    "category": category,
                    "speaker": speaker.split("/")[0],
                    "file_name": os.path.splitext(wav)[0]
                }

total_files = sum(category_counter.values())
probability_weights = {cat: round(count / total_files, 4) for cat, count in category_counter.items()}

# Step 2: Generate flattened metadata
nonverbal_metadata = {}

for file_rel_path, info in tqdm(category_files.items(), desc="Processing files"):
    file_path = os.path.join(BASE_DIR, file_rel_path)
    analysis = analyze_audio(file_path)

    category_key = info["category"]
    speaker = info["speaker"]
    file_name = info["file_name"]
    flat_key = f"{category_key}_{file_name}".replace(" ", "")

    # Ensure all values are JSON-serializable (convert to native types)

    # [w.capitalize() for w in category_key.replace('_', ' ').split()]


    metadata_entry = {
        "description": f"Sound of {split_camel_case(category_key)}.",
        "probability_weight": float(probability_weights.get(category_key, 0)),
        "file_path": file_rel_path,
        "prosody_hint": str(analysis["prosody_hint"]),
        "default_offsets": {
            "start": float(analysis["default_offsets"]["start"]),
            "end": float(analysis["default_offsets"]["end"])
        },
        "duration_range": {
            "min": float(analysis["duration_range"]["min"]),
            "max": float(analysis["duration_range"]["max"])
        },
        "amplitude_range": {
            "min": float(analysis["amplitude_range"]["min"]),
            "max": float(analysis["amplitude_range"]["max"])
        },
        "variation_params": {
            "pitch_jitter_cents": float(analysis["variation_params"]["pitch_jitter_cents"]),
            "time_jitter_pct": float(analysis["variation_params"]["time_jitter_pct"])
        },
        "transcript_marker": split_camel_case(category_key).split()[0]

    }

    nonverbal_metadata[flat_key] = metadata_entry

# Step 3: Save JSON
with open(OUTPUT_JSON, 'w') as f:
    json.dump(nonverbal_metadata, f, indent=4)

print(f"✅ Non-verbal metadata saved to {OUTPUT_JSON}")


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

with open("Dataset Preparation & Setup/Metadata/Non_verbal_cues_extended.json", "w") as f_out:
    json.dump(non_verbal_cues, f_out, indent=4)

print("non_verbal_cues_extended.json updated successfully!")

