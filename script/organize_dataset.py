

# import os
# import shutil
# import re
# import sys

# # Speaker name must match folder name exactly (case-sensitive)
# speaker_name = 'Edward'  # or 'edward' if folder is lowercase

# # Construct absolute path to the dataset
# base_dir = os.path.dirname(os.path.abspath(__file__))  # script
# source_dir = os.path.join(base_dir, '..', 'Dataset', speaker_name)
# target_base_dir = os.path.join(base_dir, '..', 'Dataset', 'project_voltron_dataset', 'male')

# # Sanity check
# if not os.path.exists(source_dir):
#     print(f"❌ ERROR: Source directory does not exist: {source_dir}")
#     sys.exit(1)

# # Create intensity folders
# intensities = ['low', 'medium', 'high']
# for intensity in intensities:
#     os.makedirs(os.path.join(target_base_dir, intensity), exist_ok=True)

# # Map common keywords to normalized intensity folder
# intensity_map = {
#     'low': 'low',
#     'low intens': 'low',
#     'medium': 'medium',
#     'med intens': 'medium',
#     'high': 'high',
#     'high intens': 'high'
# }



# take_number_pattern = re.compile(r"take[\s_]?(\d+)", re.IGNORECASE)
# i=0
# for filename in os.listdir(source_dir):
#     if not filename.lower().endswith('.wav'):
#         continue

#     fname_lower = filename.lower()
#     target_intensity = None
#     for key, mapped in intensity_map.items():
#         if key in fname_lower:
#             target_intensity = mapped
#             break

#     if not target_intensity:
#         print(f"⚠️ Skipped (no intensity): {filename}")
#         continue

#     take_match = take_number_pattern.search(fname_lower)
#     take_suffix = f"take{take_match.group(1)}" if take_match else "takeX"

#     if 'prim' in fname_lower or '(prim)' in fname_lower:
#         new_filename = f"{speaker_name}_AngerPrimary_{take_suffix}.wav"
#     elif 'primaryemotion_anger' in fname_lower:
#         new_filename = f"{speaker_name}_AngerPrimary_{take_suffix.capitalize()}.wav"
#     else:
#         new_filename = f"{speaker_name}_AngerPrimary_{take_suffix}.wav"

#     src_path = os.path.join(source_dir, filename)
#     dst_path = os.path.join(target_base_dir, target_intensity, new_filename)

#     shutil.copy2(src_path, dst_path)
#     print(f"✅ Moved: {filename} → {target_intensity}/{new_filename}")
#     i=i+1
#     print(i)

# import os
# import shutil
# import re
# import sys

# # --- Configuration ---
# speaker_name = 'Edward'  # or dynamically loop over all speaker folders
# base_dir = os.path.dirname(os.path.abspath(__file__))
# source_dir = os.path.join(base_dir, '..', 'Dataset', speaker_name)
# target_base_dir = os.path.join(base_dir, '..', 'project_voltron_dataset', 'male')

# # --- Valid categories mapping ---
# category_map = {
#     'prim': 'Primary',
#     'primary': 'Primary',
#     'primaryemotion': 'Primary',
#     'sec': 'Secondary',
#     'secondary': 'Secondary',
#     'secondaryemotion': 'Secondary'
# }

# # --- Intensity folder mapping ---
# intensity_map = {
#     'low': 'low',
#     'low intens': 'low',
#     'medium': 'medium',
#     'med intens': 'medium',
#     'high': 'high',
#     'high intens': 'high'
# }

# # --- Ensure output folders exist ---
# for intensity_folder in ['low', 'medium', 'high']:
#     os.makedirs(os.path.join(target_base_dir, intensity_folder), exist_ok=True)

# # --- Regex Patterns ---
# take_pattern = re.compile(r"take[\s_]?(\d+)", re.IGNORECASE)
# emotion_pattern = re.compile(r"(anger|joy|fear|sadness|disgust|surprise|trust|anticipation)", re.IGNORECASE)
# category_pattern = re.compile(r"(prim|primary|primaryemotion|sec|secondary|secondaryemotion)", re.IGNORECASE)
# intensity_pattern = re.compile(r"(low intens|low|medium|med intens|high intens|high)", re.IGNORECASE)

# # --- Validate path ---
# if not os.path.exists(source_dir):
#     print(f"❌ ERROR: Source directory does not exist: {source_dir}")
#     sys.exit(1)

# # --- Process files ---
# for filename in os.listdir(source_dir):
#     if not filename.lower().endswith('.wav'):
#         continue

#     fname_lower = filename.lower()

#     # Extract take number
#     take_match = take_pattern.search(fname_lower)
#     take_suffix = f"Take{take_match.group(1)}" if take_match else "TakeX"

#     # Extract intensity
#     intensity = None
#     for key, mapped in intensity_map.items():
#         if key in fname_lower:
#             intensity = mapped
#             break
#     if not intensity:
#         print(f"⚠️ Skipped (intensity not detected): {filename}")
#         continue

#     # Extract emotion
#     emotion_match = emotion_pattern.search(fname_lower)
#     emotion = emotion_match.group(1).capitalize() if emotion_match else "Unknown"

#     # Extract category
#     category_match = category_pattern.search(fname_lower)
#     category = category_map[category_match.group(1)] if category_match else "Unknown"

#     # Compose new filename
#     new_filename = f"{speaker_name}_{emotion}{category}_{take_suffix}.wav"

#     # Copy to correct folder
#     src_path = os.path.join(source_dir, filename)
#     dst_path = os.path.join(target_base_dir, intensity, new_filename)

#     shutil.copy2(src_path, dst_path)
#     print(f"✅ Moved: {filename} → {intensity}/{new_filename}")

# import os
# import re
# import shutil

# def ensure_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# def organize_dataset(source_root, dest_root):
#     for speaker in os.listdir(source_root):
#         speaker_path = os.path.join(source_root, speaker)
#         if not os.path.isdir(speaker_path):
#             continue

#         for filename in os.listdir(speaker_path):
#             if not filename.endswith('.wav'):
#                 continue

#             # Match: male_AngerPrimary_High_1.wav
#             match = re.match(r'^(male|female)_(\w+?)_(low|medium|high)_(\d+)\.wav$', filename, re.IGNORECASE)
#             if not match:
#                 print(f"Skipping unrecognized file: {filename}")
#                 continue

#             gender = match.group(1).lower()
#             emotion = match.group(2)
#             intensity = match.group(3).lower()
#             index = match.group(4)

#             # Create target folder path
#             target_dir = os.path.join(dest_root, gender, intensity)
#             ensure_dir(target_dir)

#             # New filename format: Edward_AngerPrimary_1.wav
#             new_filename = f"{speaker}_{emotion}_{index}.wav"
#             src_file = os.path.join(speaker_path, filename)
#             dst_file = os.path.join(target_dir, new_filename)

#             print(f"Moving {src_file} -> {dst_file}")
#             shutil.copy2(src_file, dst_file)  # Use copy2 to preserve timestamps if needed

# if __name__ == "__main__":
#     source_dataset_path = "Dataset"
#     output_dataset_path = "project_voltron_dataset"

#     organize_dataset(source_dataset_path, output_dataset_path)

# import os
# import re
# import shutil

# def ensure_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# def organize_dataset(source_root, dest_root):
#     for speaker in os.listdir(source_root):
#         speaker_path = os.path.join(source_root, speaker)
#         if not os.path.isdir(speaker_path):
#             continue

#         for filename in os.listdir(speaker_path):
#             if not filename.lower().endswith(".wav"):
#                 continue

#             match = re.match(r"^(male|female)_(\w+?)_(low|medium|high)_(\d+)\.wav$", filename, re.IGNORECASE)
#             if not match:
#                 print(f"[SKIP] File does not match pattern: {filename}")
#                 continue

#             gender = match.group(1).lower()
#             emotion = match.group(2)
#             intensity = match.group(3).lower()
#             index = match.group(4)

#             target_dir = os.path.join(dest_root, gender, intensity)
#             ensure_dir(target_dir)

#             new_filename = f"{speaker}_{emotion}_{index}.wav"
#             src_path = os.path.join(speaker_path, filename)
#             dst_path = os.path.join(target_dir, new_filename)

#             print(f"[COPY] {src_path} -> {dst_path}")
#             shutil.copy2(src_path, dst_path)

# if __name__ == "__main__":
#     source_dataset_path = "Dataset Preparation & Setup/Dataset"
#     output_dataset_path = "Dataset Preparation & Setup/project_voltron_dataset"

#     organize_dataset(source_dataset_path, output_dataset_path)

# 111
# import os
# import re
# import shutil

# def ensure_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# def organize_dataset(source_root, dest_root):
#     copy_logs = []
#     skip_logs = []
#     skip_count = 0
#     i=0
#     for speaker in os.listdir(source_root):
#         speaker_path = os.path.join(source_root, speaker)
#         if not os.path.isdir(speaker_path):
#             continue

#         for filename in os.listdir(speaker_path):
#             if not filename.lower().endswith(".wav"):
#                 continue

#             match = re.match(r"^(male|female)_(.+?)_(low|medium|high|unknown)?[_]?(\d*)\.wav$", filename, re.IGNORECASE)
#             if not match:
#                 skip_logs.append(f"[SKIP] Unrecognized pattern: {filename}")
#                 skip_count += 1
#                 continue

#             gender = match.group(1).lower()
#             emotion = match.group(2)
#             intensity = match.group(3)
#             index = match.group(4)

#             if not intensity or intensity.lower() == "unknown":
#                 intensity = "medium"
#             else:
#                 intensity = intensity.lower()

#             emotion = emotion.strip()

#             target_dir = os.path.join(dest_root, gender, intensity)
#             ensure_dir(target_dir)

#             new_filename = f"{speaker}_{emotion}_{index}.wav"

#             src_path = os.path.join(speaker_path, filename)
#             dst_path = os.path.join(target_dir, new_filename)

#             copy_logs.append(f"[COPY] {src_path} -> {dst_path}")
#             shutil.copy2(src_path, dst_path)
#             i=i+1
#     print(i)   

#     # Print COPY logs first
#     for log in copy_logs:
#         print(log)

#     if skip_logs:
#         print("\nSkip files are given below:")
#         for log in skip_logs:
#             print(log)

#     print(f"\nTotal skipped files: {skip_count}")

# if __name__ == "__main__":
#     source_dataset_path = "Dataset Preparation & Setup/Dataset"
#     output_dataset_path = "Dataset Preparation & Setup/project_voltron_dataset"

#     organize_dataset(source_dataset_path, output_dataset_path)

import os
import shutil
import re

# Paths
base_dir = "Dataset Preparation & Setup"
nvc_dir = os.path.join(base_dir, "NVC")
voltron_dataset_dir = os.path.join(base_dir, "project_voltron_dataset")

# Helper: Gender mapping based on folder names
gender_map = {
    "Carrie": "female",
    "Connor": "male"
}

# Create nonverbal_cues folders if not exist
for gender in ["male", "female"]:
    nvc_target_dir = os.path.join(voltron_dataset_dir, gender, "nonverbal_cues")
    os.makedirs(nvc_target_dir, exist_ok=True)

# Process NVC files
for person in os.listdir(nvc_dir):
    person_dir = os.path.join(nvc_dir, person)
    if not os.path.isdir(person_dir):
        continue

    gender = gender_map.get(person)
    if not gender:
        print(f"⚠️ Skipping unrecognized folder: {person}")
        continue

    nvc_target_dir = os.path.join(voltron_dataset_dir, gender, "nonverbal_cues")

    for file in os.listdir(person_dir):
        if file.lower().endswith('.wav'):
            src_path = os.path.join(person_dir, file)
            dest_path = os.path.join(nvc_target_dir, f"{person}_{file}")
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_path} → {dest_path}")

print("\n✅ Non-verbal cues organized successfully into project_voltron_dataset!")


    

# import os
# import re
# import shutil

# def ensure_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# def clean_emotion_name(emotion):
#     # Optional: Remove extra whitespace
#     emotion = emotion.strip()
#     # Replace spaces with underscores (optional, for clarity)
#     emotion = emotion.replace(" ", "_")
#     return emotion

# def organize_dataset(source_root, dest_root):
#     for speaker in os.listdir(source_root):
#         speaker_path = os.path.join(source_root, speaker)
#         if not os.path.isdir(speaker_path):
#             continue

#         for filename in os.listdir(speaker_path):
#             if not filename.lower().endswith(".wav"):
#                 continue

#             # Flexible regex: match gender + emotion + optional intensity + optional index
#             match = re.match(r"^(male|female)_(.+?)(?:_(low|medium|high|unknown))?(?:_(\d+))?\.wav$", filename, re.IGNORECASE)
#             if match:
#                 gender = match.group(1).lower()
#                 emotion = match.group(2)
#                 intensity = match.group(3)
#                 index = match.group(4)
#             else:
#                 # Fallback: match only gender and emotion (no intensity/index)
#                 fallback_match = re.match(r"^(male|female)_(.+?)\.wav$", filename, re.IGNORECASE)
#                 if fallback_match:
#                     gender = fallback_match.group(1).lower()
#                     emotion = fallback_match.group(2)
#                     intensity = None
#                     index = None
#                 else:
#                     print(f"[SKIP] Could not match pattern: {filename}")
#                     continue

#             # Default intensity to 'medium' if missing or 'unknown'
#             if not intensity or intensity.lower() == "unknown":
#                 intensity = "medium"
#             else:
#                 intensity = intensity.lower()

#             # Default index to 1 if missing
#             if not index:
#                 index = "1"

#             # Clean emotion name
#             emotion = clean_emotion_name(emotion)

#             target_dir = os.path.join(dest_root, gender, intensity)
#             ensure_dir(target_dir)

#             new_filename = f"{speaker}_{emotion}_{index}.wav"
#             src_path = os.path.join(speaker_path, filename)
#             dst_path = os.path.join(target_dir, new_filename)

#             print(f"[COPY] {src_path} -> {dst_path}")
#             shutil.copy2(src_path, dst_path)

# if __name__ == "__main__":
#     source_dataset_path = "Dataset Preparation & Setup/Dataset"
#     output_dataset_path = "Dataset Preparation & Setup/project_voltron_dataset"

#     organize_dataset(source_dataset_path, output_dataset_path)



# import os
# import shutil
# import re

# def create_directory_structure(base_path):
#     """Create the male and female directory structure."""
#     # Define directories
#     male_path = os.path.join(base_path, "male")
#     female_path = os.path.join(base_path, "female")
#     intensities = ["low", "medium", "high"]
    
#     # Create male directories
#     os.makedirs(male_path, exist_ok=True)
#     for intensity in intensities:
#         os.makedirs(os.path.join(male_path, intensity), exist_ok=True)
    
#     # Create female directories (empty)
#     os.makedirs(female_path, exist_ok=True)
#     for intensity in intensities:
#         os.makedirs(os.path.join(female_path, intensity), exist_ok=True)

# def parse_filename(filename):
#     """Parse the filename to extract emotion, intensity, take number, and type (Primary/Secondary)."""
#     # Remove .wav extension
#     name = os.path.splitext(filename)[0]
    
#     # Extract emotion type (Primary or Secondary)
#     emotion_type = "Primary" if "PrimaryEmotion" in name else "Secondary"
    
#     # Extract intensity (Low, Medium, High)
#     intensity = None
#     if "Low" in name:
#         intensity = "low"
#     elif "Medium" in name:
#         intensity = "medium"
#     elif "High" in name:
#         intensity = "high"
    
#     # Extract take number
#     take_match = re.search(r"Take(\d+)", name)
#     take_number = take_match.group(1) if take_match else None
    
#     # Extract emotion
#     emotion = None
#     if emotion_type == "Primary":
#         # Handle special case for Joy (Happiness)
#         if "Joy (Happiness)" in name:
#             name = "Joy"
#         else:
#             # Extract emotion from PrimaryEmotion_{Emotion}_...
#             match = re.search(r"PrimaryEmotion_([A-Za-z]+)_", name)
#             emotion = match.group(1) if match else None
#     else:
#         # Extract emotion from SecondaryEmotion_{Emotion}_...
#         match = re.search(r"SecondaryEmotion_([A-Za-z]+)_", name)
#         emotion = match.group(1) if match else None
    
#     return emotion, intensity, take_number, emotion_type

# def organize_dataset(input_path):
#     """Organize audio files into the specified directory structure."""
#     # Create directory structure
#     create_directory_structure(input_path)
#     i=0
#     # Get list of WAV files
#     wav_files = [f for f in os.listdir(input_path) if f.endswith(".wav")]
    
#     for wav_file in wav_files:
#         # Parse filename
#         emotion, intensity, take_number, emotion_type = parse_filename(wav_file)
        
#         if not all([emotion, intensity, take_number, emotion_type]):
#             print(f"Skipping {wav_file}: Unable to parse filename")
#             continue
        
#         # Construct new filename (e.g., AngerPrimary_Take2.wav)
#         new_filename = f"{emotion}{emotion_type}_Take{take_number}.wav"
        
#         # Determine destination path (male/{intensity}/)
#         dest_dir = os.path.join(input_path, "male", intensity)
#         dest_path = os.path.join(dest_dir, new_filename)
        
#         # Move file to destination
#         src_path = os.path.join(input_path, wav_file)
#         try:
#             shutil.move(src_path, dest_path)
#             print(f"Moved {wav_file} to {dest_path}")
#         except Exception as e:
#             print(f"Error moving {wav_file}: {e}")
#         i=i+1
#     print(i)
# def main():
#     # Define base path
#     base_path = os.path.expanduser("Dataset Preparation & Setup/Dataset/Edward")
    
#     # Organize dataset
#     organize_dataset(base_path)

# if __name__ == "__main__":
#     main()


# import os
# import shutil
# import re

# def create_directory_structure(base_path):
#     """Create the male and female directory structure."""
#     male_path = os.path.join(base_path, "male")
#     female_path = os.path.join(base_path, "female")
#     intensities = ["low", "medium", "high"]

#     os.makedirs(male_path, exist_ok=True)
#     os.makedirs(female_path, exist_ok=True)

#     for intensity in intensities:
#         os.makedirs(os.path.join(male_path, intensity), exist_ok=True)
#         os.makedirs(os.path.join(female_path, intensity), exist_ok=True)

# def parse_filename(filename):
#     """Parse the filename to extract emotion, intensity, take number, and type (Primary/Secondary)."""
#     name = os.path.splitext(filename)[0]
#     emotion_type = "Primary" if "PrimaryEmotion" in name else "Secondary"

#     # Extract intensity
#     intensity = None
#     if re.search(r"low", name, re.IGNORECASE):
#         intensity = "low"
#     elif re.search(r"medium", name, re.IGNORECASE):
#         intensity = "medium"
#     elif re.search(r"high", name, re.IGNORECASE):
#         intensity = "high"

#     # Extract take number
#     take_match = re.search(r"Take(\d+)", name, re.IGNORECASE)
#     take_number = take_match.group(1) if take_match else None

#     # Extract emotion
#     emotion = None
#     match = re.search(r"(PrimaryEmotion|SecondaryEmotion)_([A-Za-z]+)", name)
#     if match:
#         emotion = match.group(2)

#     return emotion, intensity, take_number, emotion_type

# def organize_dataset(base_path):
#     """Organize audio files into the male/female directory structure based on speaker and filename."""
#     create_directory_structure(base_path)
#     speaker_genders = {
#         "Carrie": "female",
#         "Julie": "female",
#         "Natalia": "female",
#         "Edward": "male",
#         "Jayson": "male",
#         "Connor": "male"
#     }

#     total_files = 0
#     for speaker in os.listdir(base_path):
#         speaker_path = os.path.join(base_path, speaker)
#         if not os.path.isdir(speaker_path) or speaker.lower() in ["male", "female"]:
#             continue

#         gender = speaker_genders.get(speaker, "male")  # Default to male if not listed

#         for wav_file in os.listdir(speaker_path):
#             if not wav_file.endswith(".wav"):
#                 continue

#             emotion, intensity, take_number, emotion_type = parse_filename(wav_file)
#             if not all([emotion, intensity, take_number, emotion_type]):
#                 print(f"Skipping {wav_file}: Unable to parse filename")
#                 continue

#             new_filename = f"{emotion}{emotion_type}_Take{take_number}.wav"
#             dest_dir = os.path.join(base_path, gender, intensity)
#             dest_path = os.path.join(dest_dir, new_filename)

#             src_path = os.path.join(speaker_path, wav_file)
#             try:
#                 shutil.move(src_path, dest_path)
#                 print(f"✅ Moved {wav_file} to {dest_path}")
#                 total_files += 1
#             except Exception as e:
#                 print(f"❌ Error moving {wav_file}: {e}")

#     print(f"\n🎉 Total files moved: {total_files}")

# def main():
#     base_path = "Dataset Preparation & Setup/Dataset"
#     organize_dataset(base_path)

# if __name__ == "__main__":
#     main()

