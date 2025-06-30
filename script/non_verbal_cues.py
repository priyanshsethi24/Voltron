import json

# Provided non-verbal cue labels with IDs
non_verbal_cues = [
    { "id": 1, "label": "Laughter_Soft_Chuckle_1" },
    { "id": 2, "label": "Laughter_Hearty_1" },
    { "id": 3, "label": "Laughter_Nervous" },
    { "id": 4, "label": "Laughter_Polite" },
    { "id": 5, "label": "Laughter_Speaking_1" },
    { "id": 6, "label": "Sigh_Relieved" },
    { "id": 7, "label": "Sigh_Exasperated" },
    { "id": 8, "label": "Sigh_Contented" },
    { "id": 9, "label": "Sigh_Frustrated_1" },
    { "id": 10, "label": "Sigh_Bored" },
    { "id": 11, "label": "Gasp_Surprised_1" },
    { "id": 12, "label": "Gasp_Shocked" },
    { "id": 13, "label": "Gasp_Realization" },
    { "id": 14, "label": "Gasp_Dramatic_1" },
    { "id": 15, "label": "Gasp_Mild" },
    { "id": 16, "label": "Pause_Thoughtful_1" },
    { "id": 17, "label": "Breath_Deep" },
    { "id": 18, "label": "Breath_Heavy" },
    { "id": 19, "label": "Breath_Calm" },
    { "id": 20, "label": "Inhale_Quick_1" },
    { "id": 21, "label": "Hum_Agreement_1" },
    { "id": 22, "label": "Murmur_Uncertain" },
    { "id": 23, "label": "Murmur_Pondering_1" },
    { "id": 24, "label": "Hum_Tune" },
    { "id": 25, "label": "Murmur_Soft" },
    { "id": 26, "label": "Cough_Polite" },
    { "id": 27, "label": "Throat_Clear_Nervous" },
    { "id": 28, "label": "Cough_Light" },
    { "id": 29, "label": "Throat_Clear_Preparing_1" },
    { "id": 30, "label": "Cough_Playful" },
    { "id": 31, "label": "Sniffle_Emotional" },
    { "id": 32, "label": "Sob_Light" },
    { "id": 33, "label": "Cry_Joy" },
    { "id": 34, "label": "Cry_Frustrated" },
    { "id": 35, "label": "Tear_Up" },
    { "id": 36, "label": "Applause_Subtle" },
    { "id": 37, "label": "Cheer_Excited_1" },
    { "id": 38, "label": "Clap_Playful" },
    { "id": 39, "label": "Cheer_Enthusiastic" },
    { "id": 40, "label": "Clap_Slow" },
    { "id": 41, "label": "Yawn_Exhausted_1" },
    { "id": 42, "label": "Shush" },
    { "id": 43, "label": "Lip_Smack" },
    { "id": 44, "label": "Whistle_Playful" },
    { "id": 45, "label": "Hiccup" },
    { "id": 46, "label": "Inhale_Quick_2" },
    { "id": 47, "label": "Hum_Agreement_2" },
    { "id": 48, "label": "Cheer_Excited_2" },
    { "id": 49, "label": "Gasp_Surprised_2" },
    { "id": 50, "label": "Sigh_Frustrated_2" },
    { "id": 51, "label": "Throat_Clear_Preparing_2" },
    { "id": 52, "label": "Laughter_Soft_Chuckle_2" },
    { "id": 53, "label": "Gasp_Dramatic_2" },
    { "id": 54, "label": "Murmur_Pondering_2" },
    { "id": 55, "label": "Laughter_Speaking_2" },
    { "id": 56, "label": "Pause_Natural" },
    { "id": 57, "label": "Pause_Reflective" },
    { "id": 58, "label": "Pause_Pondering" },
    { "id": 59, "label": "Pause_Thoughtful_2" },
    { "id": 60, "label": "Pause_Realization" },
    { "id": 61, "label": "Sigh_Realization" },
    { "id": 62, "label": "Sigh_Reflective" },
    { "id": 63, "label": "Sigh_Regretful" },
    { "id": 64, "label": "Sigh_Resigned" },
    { "id": 65, "label": "Sigh_Determined" },
    { "id": 66, "label": "Laughter_Hearty_2" },
    { "id": 67, "label": "Laughter_Surprised" },
    { "id": 68, "label": "Laughter_Quick" },
    { "id": 69, "label": "Laughter_Disbelief" },
    { "id": 70, "label": "Laughter_Playful" },
    { "id": 71, "label": "Gasp_Amazement" },
    { "id": 72, "label": "Gasp_Overwhelmed" },
    { "id": 73, "label": "Gasp_Shock" },
    { "id": 74, "label": "Gasp_Joyful" },
    { "id": 75, "label": "Gasp_Surprised_Delight" },
    { "id": 76, "label": "Groan_Annoyed" },
    { "id": 77, "label": "Moan_Content" },
    { "id": 78, "label": "Groan_Exasperated" },
    { "id": 79, "label": "Moan_Doubtful" },
    { "id": 80, "label": "Click_Disapproval" },
    { "id": 81, "label": "Click_Pondering" },
    { "id": 82, "label": "Pop_Surprised" },
    { "id": 83, "label": "Exhale_Relief" },
    { "id": 84, "label": "Exhale_Surprise" },
    { "id": 85, "label": "Exhale_Nervous" },
    { "id": 86, "label": "Grunt_Approval" },
    { "id": 87, "label": "Grunt_Agreement" },
    { "id": 88, "label": "Grunt_Irritated" },
    { "id": 89, "label": "Snort_Amused" },
    { "id": 90, "label": "Snort_Skeptical" },
    { "id": 91, "label": "Snort_Surprised" },
    { "id": 92, "label": "Whisper_Secretive" },
    { "id": 93, "label": "Whisper_Confidential" },
    { "id": 94, "label": "Whisper_Alert" },
    { "id": 95, "label": "Shiver_Cold" },
    { "id": 96, "label": "Shudder_Disgust" },
    { "id": 97, "label": "Shiver_Fearful" },
    { "id": 98, "label": "Sneeze_Loud" },
    { "id": 99, "label": "Sneeze_With_Sniffles" },
    { "id": 100,"label": "Sneeze_Polite" },
    { "id": 101,"label": "Yawn_Exhausted_2" },
    { "id": 102,"label": "Yawn_Interrupted" },
    { "id": 103,"label": "Yawn_Bored" },
    { "id": 104,"label": "Chatter_Teeth_Cold" },
    { "id": 105,"label": "Chatter_Teeth_Shivering" },
    { "id": 106,"label": "Groggy_Sleepy" },
    { "id": 107,"label": "Groggy_Unfocused" },
    { "id": 108,"label": "Groggy_Confused" },
    { "id": 109,"label": "Imitative_Horn" },
    { "id": 110,"label": "Imitative_Explosion" },
    { "id": 111,"label": "Imitative_Tapping" },
    { "id": 112,"label": "Nonverbal_Affirmation" },
    { "id": 113,"label": "Nonverbal_Approval" },
    { "id": 114,"label": "Nonverbal_Quick_Agree" },
    { "id": 115,"label": "Nonverbal_Disapproval" },
    { "id": 116,"label": "Nonverbal_Disagree" },
    { "id": 117,"label": "Nonverbal_Skeptical" }
]

# Save as JSON
file_path = "non_verbal_labels.json"
with open(file_path, "w") as f:
    json.dump(non_verbal_cues, f, indent=2)

# Generated code path

# import os
# import shutil
# import re

# # Define base and source directories
# base_dir = "Dataset Preparation & Setup"
# source_dirs = ['Carrie_Non_verbal_cues', 'Connor_Non_verbal_cues']
# destination_dir = "Dataset Preparation & Setup/NVC"

# def clean_filename(filename: str, gender_prefix: str) -> str:
#     # Step 1: Remove timestamp pattern and any extra spaces
#     filename = re.sub(r'[-–]\s*\d{4}-\d{1,2}-\d{1,2},?\s*\d{1,2}\.\d{1,2}[\u200E\s]*[APap][Mm]', '', filename)
#     filename = filename.strip()

#     # Step 2: Remove extension and unify separators
#     filename_wo_ext = os.path.splitext(filename)[0]
#     parts = re.split(r'[._\s\-]+', filename_wo_ext)

#     # Step 3: Remove redundant gender indicators (e.g., "Female", "Male") from parts
#     parts = [p for p in parts if p.lower() != gender_prefix.lower()]

#     # Step 4: Capitalize each part for camel-like formatting (e.g., CryJoy)
#     cleaned_name = gender_prefix + '_' + ''.join(part.capitalize() for part in parts)

#     return cleaned_name + '.wav'

# # Iterate through each source directory
# for src in source_dirs:
#     gender_prefix = 'Female' if 'Carrie' in src else 'Male'
#     src_path = os.path.join(base_dir, src)
    
#     for file in os.listdir(src_path):
#         if file.lower().endswith('.wav'):
#             old_path = os.path.join(src_path, file)
#             new_filename = clean_filename(file, gender_prefix)
#             new_path = os.path.join(destination_dir, new_filename)
            
#             shutil.copy2(old_path, new_path)
#             print(f"Copied: {old_path} → {new_path}")

# print("\n✅ All non-verbal cue files renamed and copied successfully.")

# import os
# import shutil
# import re

# # Define base and source directories
# base_dir = "Dataset Preparation & Setup"
# source_dirs = ['Carrie_Non_verbal_cues', 'Connor_Non_verbal_cues']
# destination_dir = "Dataset Preparation & Setup/NVC"

# def clean_filename(filename: str, gender_prefix: str) -> str:
#     # Step 1: Remove timestamp pattern and any extra spaces
#     filename = re.sub(r'[-–]\s*\d{4}-\d{1,2}-\d{1,2},?\s*\d{1,2}\.\d{1,2}[\u200E\s]*[APap][Mm]', '', filename)
#     filename = filename.strip()

#     # Step 2: Remove extension and unify separators
#     filename_wo_ext = os.path.splitext(filename)[0]
#     parts = re.split(r'[._\s\-]+', filename_wo_ext)

#     # Step 3: Remove redundant gender indicators (e.g., "Female", "Male") from parts
#     parts = [p for p in parts if p.lower() != gender_prefix.lower()]

#     # Step 4: Capitalize each part for camel-like formatting (e.g., CryJoy)
#     cleaned_name = gender_prefix + '_' + ''.join(part.capitalize() for part in parts)

#     return cleaned_name + '.wav'

# # Iterate through each source directory
# for src in source_dirs:
#     gender_prefix = 'Female' if 'Carrie' in src else 'Male'
#     src_path = os.path.join(base_dir, src)

#     # Create target subfolder (Carrie or Connor) inside NVC
#     target_subfolder = src.split('_')[0]  # Carrie or Connor
#     target_dir = os.path.join(destination_dir, target_subfolder)
#     os.makedirs(target_dir, exist_ok=True)

#     for file in os.listdir(src_path):
#         if file.lower().endswith('.wav'):
#             old_path = os.path.join(src_path, file)
#             new_filename = clean_filename(file, gender_prefix)
#             new_path = os.path.join(target_dir, new_filename)
            
#             shutil.copy2(old_path, new_path)
#             print(f"Copied: {old_path} → {new_path}")

# print("\n✅ All non-verbal cue files renamed, copied, and organized into subfolders successfully.")



# import os
# import shutil
# import re
# from collections import defaultdict

# # Define base and source directories
# base_dir = "Dataset Preparation & Setup"
# source_dirs = ['Carrie_Non_verbal_cues', 'Connor_Non_verbal_cues']
# destination_dir = os.path.join(base_dir, "NVC")

# def clean_filename(filename: str, gender_prefix: str) -> str:
#     # Step 1: Remove timestamp pattern and any extra spaces
#     filename = re.sub(r'[-–]\s*\d{4}-\d{1,2}-\d{1,2},?\s*\d{1,2}\.\d{1,2}[\u200E\s]*[APap][Mm]', '', filename)
#     filename = filename.strip()

#     # Step 2: Remove extension and unify separators
#     filename_wo_ext = os.path.splitext(filename)[0]
#     parts = re.split(r'[._\s\-]+', filename_wo_ext)

#     # Step 3: Remove redundant gender indicators (e.g., "Female", "Male") from parts
#     parts = [p for p in parts if p.lower() != gender_prefix.lower()]

#     # Step 4: Capitalize each part for camel-like formatting (e.g., CryJoy)
#     cleaned_name = gender_prefix + '_' + ''.join(part.capitalize() for part in parts)

#     return cleaned_name + '.wav'

# # Track filenames to handle duplicates
# filename_counter = defaultdict(int)

# # Iterate through each source directory
# for src in source_dirs:
#     gender_prefix = 'Female' if 'Carrie' in src else 'Male'
#     src_path = os.path.join(base_dir, src)

#     # Create target subfolder (Carrie or Connor) inside NVC
#     target_subfolder = src.split('_')[0]  # Carrie or Connor
#     target_dir = os.path.join(destination_dir, target_subfolder)
#     os.makedirs(target_dir, exist_ok=True)

#     for file in os.listdir(src_path):
#         if file.lower().endswith('.wav'):
#             old_path = os.path.join(src_path, file)
#             base_filename = clean_filename(file, gender_prefix)

#             # Check for duplicates
#             if filename_counter[base_filename] == 0:
#                 new_filename = base_filename
#             else:
#                 name, ext = os.path.splitext(base_filename)
#                 new_filename = f"{name}{filename_counter[base_filename]}.wav"

#             filename_counter[base_filename] += 1

#             new_path = os.path.join(target_dir, new_filename)
#             shutil.copy2(old_path, new_path)
#             print(f"Copied: {old_path} → {new_path}")

# print("\n✅ All non-verbal cue files renamed, copied, and organized into subfolders successfully.")



# import os
# import shutil

# def organize_nonverbal_cues(base_path):
#     for gender in ['male', 'female']:
#         cues_path = os.path.join(base_path, gender, 'nonverbal_cues')
#         if not os.path.exists(cues_path):
#             print(f"Directory not found: {cues_path}")
#             continue

#         for filename in os.listdir(cues_path):
#             if filename.lower().endswith('.wav'):
#                 file_path = os.path.join(cues_path, filename)
#                 name_parts = filename[:-4].split('_')  # Remove '.wav' and split
#                 if len(name_parts) < 2:
#                     print(f"Filename format unexpected: {filename}")
#                     continue

#                 speaker = name_parts[0]
#                 cue = '_'.join(name_parts[1:])

#                 cue_dir = os.path.join(cues_path, cue)
#                 os.makedirs(cue_dir, exist_ok=True)

#                 new_filename = f"{speaker}.wav"
#                 new_file_path = os.path.join(cue_dir, new_filename)

#                 shutil.move(file_path, new_file_path)
#                 print(f"Moved '{filename}' to '{new_file_path}'")
# # Dataset Preparation & Setup/project_voltron_dataset/female
# if __name__ == "__main__":
#     base_dataset_path = "Dataset Preparation & Setup/project_voltron_dataset"
#     organize_nonverbal_cues(base_dataset_path)


# Generated code path
# import os
# import shutil
# import re

# # Paths
# base_dir = "Dataset Preparation & Setup"
# nvc_dir = os.path.join(base_dir, "NVC")
# voltron_dataset_dir = os.path.join(base_dir, "project_voltron_dataset")

# # Helper: Gender mapping based on folder names
# gender_map = {
#     "Carrie": "female",
#     "Connor": "male"
# }

# # Create nonverbal_cues folders if not exist
# for gender in ["male", "female"]:
#     nvc_target_dir = os.path.join(voltron_dataset_dir, gender, "nonverbal_cues")
#     os.makedirs(nvc_target_dir, exist_ok=True)

# # Process NVC files
# for person in os.listdir(nvc_dir):
#     person_dir = os.path.join(nvc_dir, person)
#     if not os.path.isdir(person_dir):
#         continue

#     gender = gender_map.get(person)
#     if not gender:
#         print(f"⚠️ Skipping unrecognized folder: {person}")
#         continue

#     nvc_target_dir = os.path.join(voltron_dataset_dir, gender, "nonverbal_cues")

#     for file in os.listdir(person_dir):
#         if file.lower().endswith('.wav'):
#             src_path = os.path.join(person_dir, file)
#             dest_path = os.path.join(nvc_target_dir, f"{person}_{file}")
#             shutil.copy2(src_path, dest_path)
#             print(f"Copied: {src_path} → {dest_path}")

# print("\n✅ Non-verbal cues organized successfully into project_voltron_dataset!")
