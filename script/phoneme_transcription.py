from textgrid import TextGrid
import json, glob, os

# Define input and output paths
base_dir = "Dataset Preparation & Setup/project_voltron_dataset/alignments"
output_path = os.path.join("Dataset Preparation & Setup/Metadata", 'phoneme_transcriptions.json')

out = {}

# Recursively search for TextGrid files in subdirectories
for root, _, _ in os.walk(base_dir):
    for tg_file in glob.glob(os.path.join(root, "*.TextGrid")):
        tg = TextGrid()
        tg.read(tg_file)
        entry = {
            "xmin":    tg.minTime,
            "xmax":    tg.maxTime,
            "tiers":   []
        }
        for tier in tg.tiers:
            intervals = [
                {"start": iv.minTime, "end": iv.maxTime, "text": iv.mark}
                for iv in tier.intervals
            ]
            entry["tiers"].append({
                "name":      tier.name,
                "type":      "IntervalTier",
                "xmin":      tier.minTime,
                "xmax":      tier.maxTime,
                "intervals": intervals
            })

        # Add file_type and object_class manually (since textgrid doesn't have them)
        entry["file_type"] = "ooTextFile"
        entry["object_class"] = "TextGrid"

        # Build the .wav name with intensity
        # Extract gender and intensity from the folder structure
        rel_path = os.path.relpath(tg_file, base_dir)
        parts = rel_path.split(os.sep)
        if len(parts) >= 3:
            gender = parts[0]
            intensity = parts[1]
            file_stem = os.path.basename(tg_file).replace(".TextGrid", "")
            wav_name = f"{intensity}/{file_stem}.wav"
            out[wav_name] = entry
        else:
            print(f"⚠️ Skipping file with unexpected folder structure: {tg_file}")

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the JSON file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(f"✔ phoneme_transcriptions.json generated at {output_path}")


# import os
# import json

# # Path to the alignment directory
# ALIGNMENTS_DIR = 'Dataset Preparation & Setup/project_voltron_dataset/alignments'

# # Output file (or you can overwrite the original if needed)

# OUTPUT_JSON = 'Dataset Preparation & Setup/Metadata/phoneme_transcriptions.json'

# # Function to traverse and map the file paths
# def map_textgrid_keys(base_dir):
#     updated_json = {}

#     for root, dirs, files in os.walk(base_dir):
#         for file in files:
#             if file.endswith('.TextGrid'):
#                 textgrid_path = os.path.join(root, file)
#                 # Extract base name without extension
#                 base_name = os.path.splitext(file)[0]

#                 # Reconstruct the corresponding .wav file path
#                 # For example: .../female/low/Julie_Suspicion(SocialEmotions)_2.TextGrid
#                 # --> project_voltron_dataset/female/low/Julie_Suspicion(SocialEmotions)_2.wav
#                 relative_path = os.path.relpath(textgrid_path, base_dir)
#                 parts = relative_path.split(os.sep)
#                 if len(parts) >= 3:  # Example: female/low/Julie_*.TextGrid
#                     gender = parts[0]
#                     intensity = parts[1]
#                     filename = parts[2].replace('.TextGrid', '.wav')

#                     wav_key = f'project_voltron_dataset/{gender}/{intensity}/{filename}'

#                     # Read the JSON content of the TextGrid file
#                     with open(textgrid_path, 'r', encoding='utf-8') as f:
#                         try:
#                             data = json.load(f)
#                             updated_json[wav_key] = data
#                         except Exception as e:
#                             print(f"Error reading {textgrid_path}: {e}")
#     return updated_json

# # Run the script
# if __name__ == '__main__':
#     result = map_textgrid_keys(ALIGNMENTS_DIR)

#     # Save to JSON
#     with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
#         json.dump(result, f, indent=2)

#     print(f"Converted JSON saved to {OUTPUT_JSON}")
