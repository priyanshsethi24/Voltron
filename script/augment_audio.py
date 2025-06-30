# import os
# import librosa
# import soundfile as sf
# from pydub import AudioSegment
# import pandas as pd
# import numpy as np
# from pathlib import Path
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# # Define paths
# INPUT_ROOT = "normalized_dataset"
# ORIGINAL_ROOT = "project_voltron_dataset"
# OUTPUT_ROOT = "augmented_dataset"
# METADATA_CSV = "metadata.csv"
# OUTPUT_CSV = "metadata_augmented.csv"

# # Augmentation parameters
# PITCH_SHIFTS = [2, -2]  # Semitones (up and down)
# TEMPO_FACTORS = [0.8, 1.2]  # Slow and fast
# INTENSITY_SHIFTS = [6, -6]  # dB (louder and quieter)

# def ensure_output_directory(output_path):
#     """Create output directory if it doesn't exist"""
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

# def apply_pitch_shift(audio_data, sample_rate, n_steps):
#     """Apply pitch shift using librosa"""
#     try:
#         return librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=n_steps)
#     except Exception as e:
#         logging.error(f"Error in pitch shift: {str(e)}")
#         return audio_data

# def apply_tempo_shift(audio_data, sample_rate, factor):
#     """Apply tempo shift using librosa"""
#     try:
#         return librosa.effects.time_stretch(audio_data, rate=factor)
#     except Exception as e:
#         logging.error(f"Error in tempo shift: {str(e)}")
#         return audio_data

# def apply_intensity_shift(audio_path, output_path, db_shift):
#     """Apply intensity shift using pydub"""
#     try:
#         audio = AudioSegment.from_wav(audio_path)
#         audio_shifted = audio + db_shift  # Adjust gain in dB
#         ensure_output_directory(output_path)
#         audio_shifted.export(output_path, format="wav")
#         return True
#     except Exception as e:
#         logging.error(f"Error in intensity shift: {str(e)}")
#         return False

# def augment_audio_file(input_path, output_base_path, filename):
#     """Augment a single audio file with pitch, tempo, and intensity variations"""
#     augmented_files = []
#     try:
#         # Load audio
#         audio_data, sample_rate = librosa.load(input_path, sr=None, mono=True)

#         # Pitch shifts
#         for n_steps in PITCH_SHIFTS:
#             output_path = f"{output_base_path}_pitch_{'up' if n_steps > 0 else 'down'}{abs(n_steps)}.wav"
#             shifted_audio = apply_pitch_shift(audio_data, sample_rate, n_steps)
#             ensure_output_directory(output_path)
#             sf.write(output_path, shifted_audio, sample_rate)
#             augmented_files.append((output_path, f"pitch_{'up' if n_steps > 0 else 'down'}{abs(n_steps)}"))
#             logging.info(f"Generated: {output_path}")

#         # Tempo shifts
#         for factor in TEMPO_FACTORS:
#             output_path = f"{output_base_path}_tempo_{'fast' if factor < 1 else 'slow'}.wav"
#             shifted_audio = apply_tempo_shift(audio_data, sample_rate, factor)
#             ensure_output_directory(output_path)
#             sf.write(output_path, shifted_audio, sample_rate)
#             augmented_files.append((output_path, f"tempo_{'fast' if factor < 1 else 'slow'}"))
#             logging.info(f"Generated: {output_path}")

#         # Intensity shifts
#         for db_shift in INTENSITY_SHIFTS:
#             output_path = f"{output_base_path}_intensity_{'louder' if db_shift > 0 else 'quieter'}.wav"
#             success = apply_intensity_shift(input_path, output_path, db_shift)
#             if success:
#                 augmented_files.append((output_path, f"intensity_{'louder' if db_shift > 0 else 'quieter'}"))
#                 logging.info(f"Generated: {output_path}")

#         return augmented_files
#     except Exception as e:
#         logging.error(f"Error augmenting {input_path}: {str(e)}")
#         return []

# def process_dataset():
#     """Process dataset to generate augmented audio and update metadata"""
#     logging.info("Starting speech augmentation...")

#     # Load metadata
#     df = pd.read_csv(METADATA_CSV)
#     new_rows = []

#     for idx, row in df.iterrows():
#         input_filepath = row['filepath']
#         # Convert original dataset path to normalized dataset path
#         normalized_filepath = input_filepath.replace(ORIGINAL_ROOT, INPUT_ROOT)
#         filename = Path(normalized_filepath).name
#         rel_path = Path(normalized_filepath).relative_to(INPUT_ROOT)
#         output_base_path = os.path.join(OUTPUT_ROOT, rel_path).replace('.wav', '')

#         if not os.path.exists(normalized_filepath):
#             logging.warning(f"Normalized audio file not found: {normalized_filepath}")
#             continue

#         # Keep original file in metadata (with updated path)
#         orig_row = row.to_dict()
#         orig_row['filepath'] = normalized_filepath
#         new_rows.append(orig_row)

#         # Generate augmented files
#         augmented_files = augment_audio_file(normalized_filepath, output_base_path, filename)
#         for aug_path, aug_type in augmented_files:
#             aug_row = row.to_dict()
#             aug_row['filepath'] = aug_path
#             aug_row['augmentation_type'] = aug_type
#             new_rows.append(aug_row)

#     # Create updated metadata DataFrame
#     aug_df = pd.DataFrame(new_rows)
#     if 'augmentation_type' not in aug_df.columns:
#         aug_df['augmentation_type'] = ''
#     aug_df['augmentation_type'] = aug_df['augmentation_type'].fillna('none')  # Original files have no augmentation

#     # Save updated metadata
#     aug_df.to_csv(OUTPUT_CSV, index=False)
#     logging.info(f"Augmented metadata saved to: {OUTPUT_CSV}")
#     logging.info("Speech augmentation complete.")

# if __name__ == "__main__":
#     process_dataset()

import os
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path

def augment_audio(input_path, output_path, aug_type):
    """
    Apply a single augmentation to an audio file.
    aug_type: 'pitch_up', 'pitch_down', 'tempo_fast', 'tempo_slow', 'intensity_louder', 'intensity_quieter'
    """
    # Load audio
    y, sr = librosa.load(input_path, sr=24000)  # Match 24kHz dataset
    
    # Augmentation parameters
    PITCH_SHIFT_UP = 2  # Semitones
    PITCH_SHIFT_DOWN = -2
    TEMPO_FAST = 1.2  # Speed up
    TEMPO_SLOW = 0.8  # Slow down
    INTENSITY_LOUDER = 6  # dB
    INTENSITY_QUIETER = -6  # dB
    
    if aug_type == 'pitch_up':
        y_aug = librosa.effects.pitch_shift(y, sr=sr, n_steps=PITCH_SHIFT_UP)
    elif aug_type == 'pitch_down':
        y_aug = librosa.effects.pitch_shift(y, sr=sr, n_steps=PITCH_SHIFT_DOWN)
    elif aug_type == 'tempo_fast':
        y_aug = librosa.effects.time_stretch(y, rate=TEMPO_FAST)
    elif aug_type == 'tempo_slow':
        y_aug = librosa.effects.time_stretch(y, rate=TEMPO_SLOW)
    elif aug_type == 'intensity_louder':
        y_aug = y * 10 ** (INTENSITY_LOUDER / 20.0)  # Convert dB to amplitude
    elif aug_type == 'intensity_quieter':
        y_aug = y * 10 ** (INTENSITY_QUIETER / 20.0)  # Convert dB to amplitude
    else:
        raise ValueError(f"Unknown augmentation type: {aug_type}")
    
    # Save augmented audio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_aug, sr)
    print(f"Generated {output_path}")

def process_dataset(input_dir, output_dir):
    """
    Process the normalized dataset to generate augmented files, organized by augmentation type.
    """
    # Augmentation types
    aug_types = [
        'pitch_up',
        'pitch_down',
        'tempo_fast',
        'tempo_slow',
        'intensity_louder',
        'intensity_quieter'
    ]
    
    categories = ['male','female']  # Only male as per dataset
    subcategories = ['high', 'medium', 'low']
    total_files = 0
    
    for category in categories:
        for subcategory in subcategories:
            input_subdir = os.path.join(input_dir, category, subcategory)
            
            if not os.path.exists(input_subdir):
                print(f"Skipping {category}/{subcategory}: Input directory not found")
                continue
            
            print(f"Processing {category}/{subcategory}...")
            
            # Get list of audio files
            audio_files = [f for f in os.listdir(input_subdir) if f.endswith('.wav')]
            
            for audio_file in audio_files:
                input_path = os.path.join(input_subdir, audio_file)
                
                # Apply each augmentation type
                for aug_type in aug_types:
                    # Output path: augmented_dataset/{aug_type}/male/{subcategory}/{original_filename}
                    output_subdir = os.path.join(output_dir, aug_type, category, subcategory)
                    output_path = os.path.join(output_subdir, audio_file)
                    augment_audio(input_path, output_path, aug_type)
                    total_files += 1
    
    print(f"Augmentation completed. Generated {total_files} files in {output_dir}")

def main():
    # Define paths
    
    input_dir = "Dataset Preparation & Setup/normalized_dataset"
    output_dir = "Dataset Preparation & Setup/augment_dataset/"
    
    # Expand user home directory
    input_dir = os.path.expanduser(input_dir)
    output_dir = os.path.expanduser(output_dir)
    
    # Remove existing augmented dataset to avoid duplicates
    if os.path.exists(output_dir):
        print(f"Removing existing {output_dir}...")
        import shutil
        shutil.rmtree(output_dir)
    
    # Process dataset
    process_dataset(input_dir, output_dir)
    print("Speech augmentation completed.")

if __name__ == "__main__":
    main()