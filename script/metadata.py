# import os
# import csv
# import pathlib
# import pandas as pd

# # Define paths
# AUDIO_ROOT = "project_voltron_dataset"
# TRANSCRIPTION_ROOT = "Transcription"
# OUTPUT_CSV = "metadata.csv"

# def extract_metadata_from_filename(filename):
#     """Extract speaker and emotion from filename like Edward_AngerPrimary_1.wav"""
#     parts = filename.replace('.wav', '').split('_')
#     speaker = parts[0]  # e.g., Edward
#     emotion = parts[1]  # e.g., AngerPrimary
#     return speaker, emotion

# def get_transcription(transcription_path):
#     """Read transcription text from file"""
#     try:
#         with open(transcription_path, 'r', encoding='utf-8') as f:
#             return f.read().strip()
#     except FileNotFoundError:
#         print(f"Transcription file not found: {transcription_path}")
#         return ""

# def generate_metadata():
#     """Generate metadata CSV from audio and transcription files"""
#     metadata = []
    
#     # Walk through audio dataset
#     for root, _, files in os.walk(AUDIO_ROOT):
#         for file in files:
#             if file.endswith('.wav'):
#                 # Get full audio file path
#                 audio_filepath = os.path.join(root, file)
                
#                 # Extract gender and intensity from directory structure
#                 rel_path = pathlib.Path(audio_filepath).relative_to(AUDIO_ROOT)
#                 parts = rel_path.parts
#                 gender = parts[0]  # male or female
#                 intensity = parts[1] if len(parts) > 1 else ""  # high, medium, low
                
#                 # Extract speaker and emotion from filename
#                 speaker, emotion = extract_metadata_from_filename(file)
                
#                 # Construct corresponding transcription file path
#                 transcription_rel_path = os.path.join(gender, intensity, file.replace('.wav', '.txt'))
#                 transcription_path = os.path.join(TRANSCRIPTION_ROOT, transcription_rel_path)
                
#                 # Get transcription text
#                 transcription = get_transcription(transcription_path)
                
#                 # Create metadata row
#                 row = {
#                     'speaker': speaker,
#                     'gender': gender,
#                     'filepath': audio_filepath,
#                     'emotion': emotion,
#                     'intensity': intensity,
#                     'cue_t_type': '',
#                     'offset_start': '',
#                     'offset_end': '',
#                     'transcription': transcription
#                 }
#                 metadata.append(row)
    
#     # Write metadata to CSV
#     with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['speaker', 'gender', 'filepath', 'emotion', 'intensity', 
#                      'cue_t_type', 'offset_start', 'offset_end', 'transcription']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in metadata:
#             writer.writerow(row)
    
#     print(f"Metadata CSV generated at: {OUTPUT_CSV}")


# if __name__ == "__main__":
#     generate_metadata()

# data = pd.read_csv("metadata.csv")
# print(data)

# import os
# import csv
# import pathlib
# import pandas as pd
# import textgrid
# import librosa

# # Define paths

# AUDIO_ROOT = "Dataset Preparation & Setup/project_voltron_dataset"
# TRANSCRIPTION_ROOT = "Dataset Preparation & Setup/Transcription"
# TEXTGRID_ROOT = "Dataset Preparation & Setup/TextGrid_Output"
# OUTPUT_CSV = "Dataset Preparation & Setup/metadata.csv"

# def extract_metadata_from_filename(filename):
#     """Extract speaker and emotion from filename like Edward_AngerPrimary_1.wav"""
#     parts = filename.replace('.wav', '').split('_')
#     speaker = parts[0]  # e.g., Edward
#     emotion = parts[1]  # e.g., AngerPrimary
#     return speaker, emotion

# def get_transcription(transcription_path):
#     """Read transcription text from file"""
#     try:
#         with open(transcription_path, 'r', encoding='utf-8') as f:
#             return f.read().strip()
#     except FileNotFoundError:
#         print(f"Transcription file not found: {transcription_path}")
#         return ""

# def get_offsets_from_textgrid(textgrid_path):
#     """Extract offset_start and offset_end from TextGrid file"""
#     try:
#         tg = textgrid.TextGrid.fromFile(textgrid_path)
#         # Prefer 'phones' tier for precise speech boundaries, fallback to 'words'
#         tier_names = [tier.name for tier in tg.tiers]
#         tier_name = 'phones' if 'phones' in tier_names else 'words'
#         tier = next(tier for tier in tg.tiers if tier.name == tier_name)
        
#         # Find first and last non-empty intervals
#         non_empty_intervals = [interval for interval in tier if interval.mark.strip()]
#         if not non_empty_intervals:
#             print(f"No non-empty intervals in {textgrid_path}")
#             return None, None
        
#         offset_start = non_empty_intervals[0].minTime
#         offset_end = non_empty_intervals[-1].maxTime
#         return offset_start, offset_end
    
#     except Exception as e:
#         print(f"Error parsing {textgrid_path}: {str(e)}")
#         return None, None

# def get_audio_duration(audio_path):
#     """Get audio file duration as fallback for offsets"""
#     try:
#         duration = librosa.get_duration(path=audio_path)
#         return duration
#     except Exception as e:
#         print(f"Error getting duration for {audio_path}: {str(e)}")
#         return None

# def generate_metadata():
#     """Generate metadata CSV with offset_start and offset_end"""
#     metadata = []
    
#     # Walk through audio dataset
#     for root, _, files in os.walk(AUDIO_ROOT):
#         for file in files:
#             if file.endswith('.wav'):
#                 # Get full audio file path
#                 audio_filepath = os.path.join(root, file)
                
#                 # Extract gender and intensity from directory structure
#                 rel_path = pathlib.Path(audio_filepath).relative_to(AUDIO_ROOT)
#                 parts = rel_path.parts
#                 gender = parts[0]  # male or female
#                 intensity = parts[1] if len(parts) > 1 else ""  # high, medium, low
                
#                 # Extract speaker and emotion from filename
#                 speaker, emotion = extract_metadata_from_filename(file)
                
#                 # Construct corresponding transcription file path
#                 transcription_rel_path = os.path.join(gender, intensity, file.replace('.wav', '.txt'))
#                 transcription_path = os.path.join(TRANSCRIPTION_ROOT, transcription_rel_path)
                
#                 # Construct corresponding TextGrid file path
#                 textgrid_rel_path = os.path.join(gender, intensity, file.replace('.wav', '.TextGrid'))
#                 textgrid_path = os.path.join(TEXTGRID_ROOT, textgrid_rel_path)
                
#                 # Get transcription text
#                 transcription = get_transcription(transcription_path)
                
#                 # Get offset_start and offset_end
#                 offset_start, offset_end = None, None
#                 if os.path.exists(textgrid_path):
#                     offset_start, offset_end = get_offsets_from_textgrid(textgrid_path)
                
#                 # Fallback: Use audio duration if TextGrid fails
#                 if offset_start is None or offset_end is None:
#                     print(f"Using audio duration as fallback for {audio_filepath}")
#                     duration = get_audio_duration(audio_filepath)
#                     offset_start = 0.0 if duration else ""
#                     offset_end = duration if duration else ""
                
#                 # Create metadata row
#                 row = {
#                     'speaker': speaker,
#                     'gender': gender,
#                     'filepath': audio_filepath,
#                     'emotion': emotion,
#                     'intensity': intensity,
#                     'cue_t_type': '',  # Placeholder, update if needed
#                     'offset_start': offset_start,
#                     'offset_end': offset_end,
#                     'transcription': transcription
#                 }
#                 metadata.append(row)
    
#     # Write metadata to CSV
#     with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['speaker', 'gender', 'filepath', 'emotion', 'intensity', 
#                       'cue_t_type', 'offset_start', 'offset_end', 'transcription']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in metadata:
#             writer.writerow(row)
    
#     print(f"Metadata CSV generated at: {OUTPUT_CSV}")

# def main():
#     generate_metadata()
#     # Display CSV content
#     try:
#         data = pd.read_csv(OUTPUT_CSV)
#         print("\nMetadata Preview:")
#         print(data)
#     except Exception as e:
#         print(f"Error reading CSV: {str(e)}")

# if __name__ == "__main__":
#     main()


import os
import csv
import pathlib
import pandas as pd
import textgrid
import librosa

# Define paths
AUDIO_ROOT = "Dataset Preparation & Setup/project_voltron_dataset"
TRANSCRIPTION_ROOT = "Dataset Preparation & Setup/project_voltron_dataset/Transcription"
TEXTGRID_ROOT = "Dataset Preparation & Setup/project_voltron_dataset/Alignments"
OUTPUT_CSV = "Dataset Preparation & Setup/Metadata/metadata.csv"

def extract_metadata_from_filename(filename):
    """Extract speaker and emotion from filename like Edward_AngerPrimary_1.wav"""
    parts = filename.replace('.wav', '').split('_')
    if len(parts) >= 2:
        speaker = parts[0]
        emotion = parts[1]
    else:
        print(f"[Warning] Unexpected filename format: {filename}")
        speaker = parts[0] if parts else ""
        emotion = ""
    return speaker, emotion

def get_transcription(transcription_path):
    """Read transcription text from file"""
    try:
        with open(transcription_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Transcription file not found: {transcription_path}")
        return ""

def get_offsets_from_textgrid(textgrid_path):
    """Extract offset_start and offset_end from TextGrid file"""
    try:
        tg = textgrid.TextGrid.fromFile(textgrid_path)
        tier_names = [tier.name for tier in tg.tiers]
        tier_name = 'phones' if 'phones' in tier_names else 'words'
        tier = next(tier for tier in tg.tiers if tier.name == tier_name)
        non_empty_intervals = [interval for interval in tier if interval.mark.strip()]
        if not non_empty_intervals:
            print(f"No non-empty intervals in {textgrid_path}")
            return None, None
        offset_start = non_empty_intervals[0].minTime
        offset_end = non_empty_intervals[-1].maxTime
        return offset_start, offset_end
    except Exception as e:
        print(f"Error parsing {textgrid_path}: {str(e)}")
        return None, None

def get_audio_duration(audio_path):
    """Get audio file duration as fallback for offsets"""
    try:
        duration = librosa.get_duration(filename=audio_path)
        return duration
    except Exception as e:
        print(f"Error getting duration for {audio_path}: {str(e)}")
        return None

def generate_metadata():
    """Generate metadata CSV with offset_start and offset_end"""
    metadata = []
    for root, dirs, files in os.walk(AUDIO_ROOT):
        # Skip any 'nonverbal_cues' directories
        if 'nonverbal_cues' in pathlib.Path(root).parts:
            continue
        
        for file in files:
            if file.endswith('.wav'):
                audio_filepath = os.path.join(root, file)
                rel_path = pathlib.Path(audio_filepath).relative_to(AUDIO_ROOT)
                parts = rel_path.parts
                
                # Get gender and intensity (with safe indexing)
                gender = parts[0] if len(parts) > 0 else ""
                intensity = parts[1] if len(parts) > 1 else ""
                
                # Extract speaker and emotion
                speaker, emotion = extract_metadata_from_filename(file)
                
                # Build transcription and TextGrid paths
                transcription_rel_path = os.path.join(gender, intensity, file.replace('.wav', '.txt'))
                transcription_path = os.path.join(TRANSCRIPTION_ROOT, transcription_rel_path)
                
                textgrid_rel_path = os.path.join(gender, intensity, file.replace('.wav', '.TextGrid'))
                textgrid_path = os.path.join(TEXTGRID_ROOT, textgrid_rel_path)
                
                # Get transcription text
                transcription = get_transcription(transcription_path)
                
                # Get offset_start and offset_end
                offset_start, offset_end = None, None
                if os.path.exists(textgrid_path):
                    offset_start, offset_end = get_offsets_from_textgrid(textgrid_path)
                
                if offset_start is None or offset_end is None:
                    print(f"Using audio duration as fallback for {audio_filepath}")
                    duration = get_audio_duration(audio_filepath)
                    offset_start = 0.0 if duration else ""
                    offset_end = duration if duration else ""
                
                # Create metadata row
                row = {
                    'speaker': speaker,
                    'gender': gender,
                    'filepath': audio_filepath,
                    'emotion': emotion,
                    'intensity': intensity,
                    'cue_t_type': '',
                    'offset_start': offset_start,
                    'offset_end': offset_end,
                    'transcription': transcription
                }
                metadata.append(row)
    
    # Write metadata to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['speaker', 'gender', 'filepath', 'emotion', 'intensity', 'cue_t_type', 'offset_start', 'offset_end', 'transcription']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in metadata:
            writer.writerow(row)
    print(f"Metadata CSV generated at: {OUTPUT_CSV}")


def main():
    generate_metadata()
    try:
        data = pd.read_csv(OUTPUT_CSV)
        print("\nMetadata Preview:")
        print(data)
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")

if __name__ == "__main__":
    main()
