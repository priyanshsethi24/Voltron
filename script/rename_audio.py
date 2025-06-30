# import os
# import re

# # Speaker to gender mapping
# speaker_gender_map = {
#     'Edward': 'male',
#     'Julie': 'female',
#     'Natalia': 'female'
# }

# # Intensity normalization map
# intensity_map = {
#     'low': 'Low',
#     'med': 'Medium',
#     'medium': 'Medium',
#     'high': 'High',
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Emotion category normalization
# category_map = {
#     'prim': 'Primary',
#     'primary': 'Primary',
#     'sec': 'Secondary',
#     'secondary': 'Secondary',
#     'secon': 'Secondary'
# }

# # Extract emotion from filename using a smart pattern
# def extract_emotion(base):
#     # Remove known category and intensity patterns first
#     base = re.sub(r'\b(primary|secondary|prim|sec|secon)\b', '', base)
#     base = re.sub(r'\b(low|med|medium|high)(\s+intens)?\b', '', base)
#     base = re.sub(r'take\s*\d+', '', base)
#     base = base.replace('(', ' ').replace(')', ' ').strip()

#     # Split by non-alphabetic chars and choose first likely emotion
#     tokens = [word.capitalize() for word in re.findall(r'[a-z]+', base) if len(word) > 2]
#     return tokens[0] if tokens else 'Unknown'

# # Helper function to extract metadata and generate new filename
# def get_standard_filename(filename, speaker_name):
#     base = filename.lower().replace('_', ' ').replace('-', ' ')
#     gender = speaker_gender_map.get(speaker_name, 'unknown')

#     # Category (default: Primary)
#     category = 'Primary'
#     for key in category_map:
#         if key in base:
#             category = category_map[key]
#             break

#     # Intensity
#     intensity_match = re.search(r'(low|med|medium|high)(\s*intens)?', base)
#     intensity = 'Unknown'
#     if intensity_match:
#         raw = intensity_match.group(0).strip()
#         intensity = intensity_map.get(raw, raw.capitalize())

#     # Take number
#     take_match = re.search(r'take\s*(\d+)', base) or re.search(r'take(\d+)', base)
#     take_num = take_match.group(1) if take_match else '1'
#     take_str = f'Take{take_num}'

#     # Emotion
#     emotion = extract_emotion(base)

#     # Final filename
#     new_name = f"{gender}_{emotion}{category}_{intensity}_{take_str}.wav"
#     return new_name

# # ✅ Dataset directory relative to script
# root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
# root_dir = os.path.abspath(root_dir)

# # Loop through speakers and rename files
# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if os.path.isdir(speaker_path):
#         for file in os.listdir(speaker_path):
#             if file.lower().endswith('.wav'):
#                 old_path = os.path.join(speaker_path, file)
#                 new_name = get_standard_filename(file, speaker)
#                 new_path = os.path.join(speaker_path, new_name)
#                 os.rename(old_path, new_path)
#                 print(f"Renamed: {file} → {new_name}")

# import os
# import re

# # Speaker to gender mapping
# speaker_gender_map = {
#     'Edward': 'male',
#     'Julie': 'female',
#     'Natalia': 'female'
# }

# # Intensity normalization map
# intensity_map = {
#     'low': 'Low',
#     'med': 'Medium',
#     'medium': 'Medium',
#     'high': 'High',
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Emotion category normalization
# category_map = {
#     'prim': 'Primary',
#     'primary': 'Primary',
#     'secon': 'Secondary',
#     'secondary': 'Secondary'
# }

# def get_standard_filename(filename, speaker_name):
#     gender = speaker_gender_map.get(speaker_name, 'unknown')
#     file_lower = filename.lower()

#     # Handle pattern: PrimaryEmotion_Emotion_Intensity_TakeX.wav or SecondaryEmotion_Emotion_Intensity_TakeX.wav
#     structured_match = re.match(
#         r'(primaryemotion|secondaryemotion)[ _-]+([a-z]+)[ _-]+(low|med|medium|high)[ _-]+take(\d+)',
#         file_lower
#     )
#     if structured_match:
#         category_raw, emotion_raw, intensity_raw, take_num = structured_match.groups()
#         category = 'Primary' if 'primary' in category_raw else 'Secondary'
#         emotion = emotion_raw.capitalize()
#         intensity = intensity_map.get(intensity_raw, intensity_raw.capitalize())
#         return f"{gender}_{emotion}{category}_{intensity}_Take{take_num}.wav"

#     # Handle loose patterns: (Prim)(joy)(med intens)(take 1)
#     base = file_lower.replace('_', ' ').replace(')', ' ').replace('(', ' ')

#     # Try to extract take
#     take_match = re.search(r'take\s*(\d+)', base)
#     take_str = f"Take{take_match.group(1)}" if take_match else "Take1"

#     # Extract intensity
#     intensity_match = re.search(r'(low|med|medium|high)(\s+intens)?', base)
#     intensity = 'Unknown'
#     if intensity_match:
#         raw_intensity = intensity_match.group(1)
#         intensity = intensity_map.get(raw_intensity, raw_intensity.capitalize())

#     # Detect category
#     category = 'Primary'
#     for key, val in category_map.items():
#         if re.search(rf'\b{key}\b', base):
#             category = val
#             break

#     # Remove known category/intensity/take terms to find emotion
#     cleaned = base
#     for word in list(category_map.keys()) + ['emotion', 'take', 'low', 'med', 'medium', 'high', 'intens']:
#         cleaned = re.sub(rf'\b{word}\b', '', cleaned)

#     # Remaining alphanumeric tokens = possible emotion
#     remaining = re.findall(r'\b[a-z]+\b', cleaned)
#     emotion = remaining[0].capitalize() if remaining else 'Unknown'

#     return f"{gender}_{emotion}{category}_{intensity}_{take_str}.wav"

# # ✅ Root dataset directory — relative path from the script directory
# root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
# root_dir = os.path.abspath(root_dir)

# renamed_files = []
# i=0
# # Process each speaker directory
# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if os.path.isdir(speaker_path):
#         for file in os.listdir(speaker_path):
#             if file.lower().endswith('.wav'):
#                 old_path = os.path.join(speaker_path, file)
#                 new_name = get_standard_filename(file, speaker)
#                 new_path = os.path.join(speaker_path, new_name)
#                 os.rename(old_path, new_path)
#                 renamed_files.append(new_name)
#                 print(f"Renamed: {file} → {new_name}")
#                 i=i+1
#                 print(i)

# import os
# import re

# # Define gender mapping for speakers
# speaker_gender = {
#     'Edward': 'male',
#     'Julie': 'female',
#     'Natalia': 'female'
# }

# # Define emotion category mapping
# category_mapping = {
#     'prim': 'Primary',
#     'secon': 'Secondary'
# }

# # Define intensity mapping
# intensity_mapping = {
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Folder containing speaker subfolders
# root_dir = './Dataset'

# # Regex to capture format: (prim)(anger)(med intens)(take 1).wav
# pattern = re.compile(r'\((.*?)\)\((.*?)\)\((.*?)\)\((take \d+)\)\.wav', re.IGNORECASE)

# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if not os.path.isdir(speaker_path):
#         continue

#     gender = speaker_gender.get(speaker, 'unknown')

#     for filename in os.listdir(speaker_path):
#         match = pattern.match(filename)
#         if not match:
#             continue

#         category_raw, emotion_raw, intensity_raw, take_raw = match.groups()

#         category = category_mapping.get(category_raw.lower(), category_raw.capitalize())
#         emotion = emotion_raw.capitalize()
#         intensity = intensity_mapping.get(intensity_raw.lower(), intensity_raw.capitalize())
#         take = take_raw.replace(' ', '').capitalize()  # e.g., "Take1"

#         # Final name: male_AngerPrimary_Medium_Take1.wav
#         new_filename = f"{gender}_{emotion}{category}_{intensity}_{take}.wav"

#         old_file_path = os.path.join(speaker_path, filename)
#         new_file_path = os.path.join(speaker_path, new_filename)

#         os.rename(old_file_path, new_file_path)
#         print(f"Renamed: {filename} -> {new_filename}")

# For the Edward audio dataset
# import os
# import re

# # Speaker to gender mapping
# speaker_gender_map = {
#     # 'Edward': 'male',
#     # 'Connor':'male',
#     # 'Jayson':'male',
#     # 'Carrie':'female',
#     # 'Julie': 'female',
#     'Natalia': 'female'
# }

# # Intensity normalization map
# intensity_map = {
#     'low': 'Low',
#     'med': 'Medium',
#     'medium': 'Medium',
#     'high': 'High',
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Emotion category normalization
# category_map = {
#     'prim': 'Primary',
#     'primary': 'Primary',
#     'secon': 'Secondary',
#     'secondary': 'Secondary'
# }

# # Updated helper to extract the correct emotion
# def extract_emotion(base):
#     # Remove known metadata terms
#     tokens = re.findall(r'\b[a-z]+\b', base)
#     tokens = [t for t in tokens if t not in category_map and t not in intensity_map and t not in ['emotion', 'take', 'intens', 'primaryemotion', 'secondaryemotion']]
#     # Take the first long-enough token as emotion
#     for token in tokens:
#         if len(token) > 2:
#             return token.capitalize()
#     return 'Unknown'

# # Build standardized filename
# def get_standard_filename(filename, speaker_name):
#     gender = speaker_gender_map.get(speaker_name, 'unknown')
#     file_lower = filename.lower()

#     # Try to match structured pattern
#     structured_match = re.match(
#         r'(primaryemotion|secondaryemotion)[ _-]+([a-z][1-9]+)[ _-]+(low|med|medium|high)[ _-]+take[\s_]*(\d+)',
#         file_lower
#     )
#     if structured_match:
#         category_raw, emotion_raw, intensity_raw, take_num = structured_match.groups()
#         category = 'Primary' if 'primary' in category_raw else 'Secondary'
#         emotion = emotion_raw.capitalize()
#         intensity = intensity_map.get(intensity_raw, intensity_raw.capitalize())
#         return f"{gender}_{emotion}{category}_{intensity}_Take{take_num}.wav"

#     # Fallback parsing
#     base = file_lower.replace('_', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ').strip()

#     # Take number
#     take_match = re.search(r'take\s*(\d+)', base)
#     take_str = f"Take{take_match.group(1)}" if take_match else "Take1"

#     # Intensity
#     intensity_match = re.search(r'(low|med|medium|high)(\s*intens)?', base)
#     intensity = 'Unknown'
#     if intensity_match:
#         raw = intensity_match.group(0).strip()
#         intensity = intensity_map.get(raw, raw.capitalize())

#     # Category
#     category = 'Primary'
#     for key in category_map:
#         if re.search(rf'\b{key}\b', base):
#             category = category_map[key]
#             break

#     # Emotion
#     emotion = extract_emotion(base)

#     return f"{gender}_{emotion}{category}_{intensity}_{take_str}.wav"

# # Root dataset directory
# root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
# root_dir = os.path.abspath(root_dir)

# renamed_files = []
# i = 0

# # Process each speaker folder
# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if os.path.isdir(speaker_path):
#         for file in os.listdir(speaker_path):
#             if file.lower().endswith('.wav'):
#                 old_path = os.path.join(speaker_path, file)
#                 new_name = get_standard_filename(file, speaker)
#                 new_path = os.path.join(speaker_path, new_name)
#                 os.rename(old_path, new_path)
#                 renamed_files.append(new_name)
#                 i += 1
#                 print(f"{i}. Renamed: {file} → {new_name}")

# import os
# import re

# # Speaker to gender mapping
# speaker_gender_map = {
#     'Natalia': 'female'
# }

# # Intensity normalization map
# intensity_map = {
#     'low': 'Low',
#     'med': 'Medium',
#     'medium': 'Medium',
#     'high': 'High',
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Category normalization
# category_map = {
#     'primary': 'Primary',
#     'secondary': 'Secondary'
# }

# def get_standard_filename(filename, speaker_name):
#     gender = speaker_gender_map.get(speaker_name, 'unknown')
#     file_lower = filename.lower()

#     # Extract take number
#     take_match = re.search(r'take\s*(\d+)', file_lower)
#     take_str = f"Take{take_match.group(1)}" if take_match else "Take1"

#     # Extract intensity
#     intensity = 'Unknown'
#     intensity_match = re.search(r'(low|med|medium|high)(\s*intens)?', file_lower)
#     if intensity_match:
#         raw = intensity_match.group(0).strip()
#         intensity = intensity_map.get(raw, raw.capitalize())

#     # Extract category
#     category = 'Unknown'
#     for key in category_map:
#         if re.search(rf'{key}', file_lower):
#             category = category_map[key]
#             break

#     # Remove 'emotion' from filename
#     base = re.sub(r'(primaryemotion|secondaryemotion|emotion)', '', filename, flags=re.IGNORECASE)
#     base = re.sub(r'[_\-]+', ' ', base)  # Replace underscores/hyphens with spaces

#     # Extract emotion + optional number (e.g., "relief19")
#     emotion_match = re.search(r'([a-zA-Z]+)(\d*)', base)
#     if emotion_match:
#         emotion = emotion_match.group(1).capitalize()
#         emotion_number = emotion_match.group(2)
#         emotion = emotion + emotion_number if emotion_number else emotion
#     else:
#         emotion = 'Unknown'

#     return f"{gender}_{emotion}{category}_{intensity}_{take_str}.wav"

# # Root dataset directory
# root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
# root_dir = os.path.abspath(root_dir)

# renamed_files = []
# i = 0

# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if os.path.isdir(speaker_path):
#         for file in os.listdir(speaker_path):
#             if file.lower().endswith('.wav'):
#                 old_path = os.path.join(speaker_path, file)
#                 new_name = get_standard_filename(file, speaker)
#                 new_path = os.path.join(speaker_path, new_name)
#                 os.rename(old_path, new_path)
#                 renamed_files.append(new_name)
#                 i += 1
#                 print(f"{i}. Renamed: {file} → {new_name}")

# For the natalia and 
# import os
# import re

# # Speaker to gender mapping
# speaker_gender_map = {
#     'Connor': 'male',
# }

# # Intensity normalization map
# intensity_map = {
#     'low': 'Low',
#     'med': 'Medium',
#     'medium': 'Medium',
#     'high': 'High',
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Category normalization
# category_map = {
#     'primary': 'Primary',
#     'secondary': 'Secondary'
# }

# def get_standard_filename(filename, speaker_name):
#     gender = speaker_gender_map.get(speaker_name, 'unknown')
#     file_lower = filename.lower()

#     # Extract take number
#     take_match = re.search(r'take\s*(\d+)', file_lower)
#     take_str = f"Take{take_match.group(1)}" if take_match else "Take1"

#     # Extract intensity
#     intensity = 'Unknown'
#     intensity_match = re.search(r'(low|med|medium|high)(\s*intens)?', file_lower)
#     if intensity_match:
#         raw = intensity_match.group(0).strip()
#         intensity = intensity_map.get(raw, raw.capitalize())

#     # Extract category (Primary or Secondary)
#     category = ''
#     for key in category_map:
#         if re.search(rf'{key}', file_lower):
#             category = category_map[key]
#             break

#     # Extract emotion and number (if any)
#     base = re.sub(r'(primary emotion|secondary emotion|emotion)', '', filename, flags=re.IGNORECASE)
#     base = re.sub(r'[_\-]+', ' ', base)  # Replace underscores/hyphens with spaces

#     emotion_match = re.search(r'([a-zA-Z]+)(\d*)', base)
#     if emotion_match:
#         emotion = emotion_match.group(1).capitalize()
#         number = emotion_match.group(2)
#     else:
#         emotion = 'Unknown'
#         number = ''

#     # Final composition
#     if category and number:
#         final_name = f"{gender}_{emotion}{category}{number}_{intensity}_{take_str}.wav"
#     elif category:
#         final_name = f"{gender}_{emotion}{category}_{intensity}_{take_str}.wav"
#     else:
#         final_name = f"{gender}_{emotion}_{intensity}_{take_str}.wav"

#     return final_name

# # Root dataset directory
# root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
# root_dir = os.path.abspath(root_dir)

# renamed_files = []
# i = 0

# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if os.path.isdir(speaker_path):
#         for file in os.listdir(speaker_path):
#             if file.lower().endswith('.wav'):
#                 old_path = os.path.join(speaker_path, file)
#                 new_name = get_standard_filename(file, speaker)
#                 new_path = os.path.join(speaker_path, new_name)
#                 os.rename(old_path, new_path)
#                 renamed_files.append(new_name)
#                 i += 1
#                 print(f"{i}. Renamed: {file} → {new_name}")


# For the jayson audio dataset
# import os
# import re

# # Speaker to gender mapping
# speaker_gender_map = {
#     'Julie': 'female',
# }

# # Intensity normalization map
# intensity_map = {
#     'low': 'Low',
#     'med': 'Medium',
#     'medium': 'Medium',
#     'high': 'High',
#     'low intens': 'Low',
#     'med intens': 'Medium',
#     'high intens': 'High'
# }

# # Category normalization
# category_map = {
#     'primaryemotion': 'Primary',
#     'secondaryemotion': 'Secondary',
#     'primary':'Primary',
#     'secondary':'Secondary',

# }

# def get_standard_filename(filename, speaker_name):
#     gender = speaker_gender_map.get(speaker_name, '')
#     file_lower = filename.lower()

#     # Extract take number
#     take_match = re.search(r'take\s*(\d+)', file_lower)
#     take_str = f"Take{take_match.group(1)}" if take_match else "Take1"

#     # Extract intensity
#     intensity = 'Unknown'
#     intensity_match = re.search(r'(low|med|medium|high)(\s*intens)?', file_lower)
#     if intensity_match:
#         raw = intensity_match.group(0).strip()
#         intensity = intensity_map.get(raw, raw.capitalize())

#     # Remove category annotations for clarity
#     cleaned_name = re.sub(r'(primaryemotion|secondaryemotion|emotion)', '', filename, flags=re.IGNORECASE)

#     # Split by underscores/hyphens to parse components (without lowercasing!)
#     parts = re.split(r'[_\-]', cleaned_name)
#     parts = [p.strip() for p in parts if p.strip()]

#     # Identify category (Primary/Secondary)
#     category = ''
#     for key, value in category_map.items():
#         if re.search(key, file_lower):
#             category = value
#             break

#     # Description logic: Only consider as description if NOT an intensity
#     description = ''
#     if len(parts) >= 2:
#         possible_desc = parts[1]
#         if possible_desc.lower() not in ['low', 'medium', 'high']:
#             description = possible_desc

#     # Build final filename
#     emotion = parts[0]
#     if category:
#         base = f"{emotion}{category}"
#     else:
#         base = f"{emotion}"

#     if description:
#         final_name = f"{gender}_{base}({description})_{intensity}_{take_str}.wav" if gender else f"{base}({description})_{intensity}_{take_str}.wav"
#     else:
#         final_name = f"{gender}_{base}_{intensity}_{take_str}.wav" if gender else f"{base}_{intensity}_{take_str}.wav"

#     # Clean up underscores and spacing
#     final_name = re.sub(r'_+', '_', final_name).replace('__', '_')
#     final_name = final_name.replace(' )', ')').replace('( ', '(').replace('()', '')

#     return final_name.lstrip('_')

# # Root dataset directory
# root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
# root_dir = os.path.abspath(root_dir)

# renamed_files = []
# i = 0

# for speaker in os.listdir(root_dir):
#     speaker_path = os.path.join(root_dir, speaker)
#     if os.path.isdir(speaker_path):
#         for file in os.listdir(speaker_path):
#             if file.lower().endswith('.wav'):
#                 old_path = os.path.join(speaker_path, file)
#                 new_name = get_standard_filename(file, speaker)
#                 new_path = os.path.join(speaker_path, new_name)
#                 os.rename(old_path, new_path)
#                 renamed_files.append(new_name)
#                 i += 1
#                 print(f"{i}. Renamed: {file} → {new_name}")

# # For the julie
# import os

# # Specify the folder path
# folder_path = "Dataset Preparation & Setup/Dataset/Julie"

# # Iterate over files in the folder
# for filename in os.listdir(folder_path):
#     if filename.endswith(".wav") and not filename.startswith("female_"):
#         # Construct the old file path
#         old_path = os.path.join(folder_path, filename)
        
#         # Create the new filename with "female_" prefix
#         new_filename = f"female_{filename}"
#         new_path = os.path.join(folder_path, new_filename)
        
#         # Rename the file
#         os.rename(old_path, new_path)

# print("All files have been renamed successfully.")

import os
import re

# Speaker to gender mapping
speaker_gender_map = {
    'Carrie': 'female',
}

# Intensity normalization map
intensity_map = {
    'low': 'Low',
    'med': 'Medium',
    'medium': 'Medium',
    'high': 'High',
    'low intens': 'Low',
    'med intens': 'Medium',
    'high intens': 'High'
}

# Category normalization
category_map = {
    'primary': 'Primary',
    'secondary': 'Secondary'
}

def get_standard_filename(filename, speaker_name):
    gender = speaker_gender_map.get(speaker_name, 'unknown')
    file_lower = filename.lower()

    # Remove extension for processing
    base_name, ext = os.path.splitext(filename)

    # Extract take number
    take_match = re.search(r'take\s*(\d+)', file_lower)
    take_str = f"Take{take_match.group(1)}" if take_match else "Take1"

    # Extract intensity
    intensity = 'Unknown'
    intensity_match = re.search(r'(low|med|medium|high)(\s*intens)?', file_lower)
    if intensity_match:
        raw = intensity_match.group(0).strip()
        intensity = intensity_map.get(raw, raw.capitalize())

    # Extract category (Primary or Secondary)
    category = ''
    for key in category_map:
        if re.search(rf'{key}', file_lower):
            category = category_map[key]
            break

    # Clean prefixes like "primary emotion", "secondary emotion", etc.
    cleaned = re.sub(r'(primary emotion|secondary emotion|emotion)', '', base_name, flags=re.IGNORECASE)
    cleaned = cleaned.strip().replace('_', ' ').replace('-', ' ')

    # Find emotion + number (including hash)
    emotion_match = re.search(r'([a-zA-Z]+)\s*(#?\d+)?', cleaned)
    if emotion_match:
        emotion = emotion_match.group(1).capitalize()
        number = emotion_match.group(2) or ''
    else:
        emotion = 'Unknown'
        number = ''

    # Final filename assembly: emotion + category + number
    if category:
        parts = [f"{gender}_{emotion}{category}{number}"]
    else:
        parts = [f"{gender}_{emotion}{number}"]

    parts.append(f"{intensity}_{take_str}{ext}")

    final_name = '_'.join(parts)

    return final_name

# Root dataset directory
root_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')
root_dir = os.path.abspath(root_dir)

renamed_files = []
i = 0

for speaker in os.listdir(root_dir):
    speaker_path = os.path.join(root_dir, speaker)
    if os.path.isdir(speaker_path):
        for file in os.listdir(speaker_path):
            if file.lower().endswith('.wav'):
                old_path = os.path.join(speaker_path, file)
                new_name = get_standard_filename(file, speaker)

                # Check for duplicates and append (1), (2), etc. if needed
                final_name = new_name
                counter = 1
                while os.path.exists(os.path.join(speaker_path, final_name)):
                    base, ext = os.path.splitext(new_name)
                    final_name = f"{base}({counter}){ext}"
                    counter += 1

                new_path = os.path.join(speaker_path, final_name)
                os.rename(old_path, new_path)
                renamed_files.append(final_name)
                i += 1
                print(f"{i}. Renamed: {file} → {final_name}")













