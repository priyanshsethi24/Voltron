# import os
# import librosa
# import soundfile as sf
# import noisereduce as nr
# from pydub import AudioSegment
# from pathlib import Path
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# # Define paths
# INPUT_ROOT = "normalized_dataset"
# OUTPUT_ROOT = "denoised_compressed_dataset"

# # Noise reduction parameters
# NOISE_REDUCTION_FACTOR = 0.95  # Proportion of noise to remove (0 to 1)

# # Compression parameters
# COMPRESSOR_THRESHOLD = -20  # dB, levels above this are compressed
# COMPRESSOR_RATIO = 3  # 3:1 ratio for moderate compression
# COMPRESSOR_ATTACK = 5  # ms, how quickly compressor reacts
# COMPRESSOR_RELEASE = 100  # ms, how quickly compressor releases

# def ensure_output_directory(output_path):
#     """Create output directory if it doesn't exist"""
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

# def reduce_noise(audio_data, sample_rate):
#     """Apply noise reduction using noisereduce"""
#     try:
#         # Estimate noise profile from the first 0.5 seconds (assumed to be silence/noise)
#         noise_clip = audio_data[:int(0.5 * sample_rate)]
#         # Apply noise reduction
#         reduced_audio = nr.reduce_noise(
#             y=audio_data,
#             sr=sample_rate,
#             y_noise=noise_clip,
#             prop_decrease=NOISE_REDUCTION_FACTOR
#         )
#         return reduced_audio
#     except Exception as e:
#         logging.error(f"Error in noise reduction: {str(e)}")
#         return audio_data  # Return original if noise reduction fails

# def apply_compression(audio_path, output_path):
#     """Apply dynamic range compression using pydub"""
#     try:
#         # Load audio with pydub
#         audio = AudioSegment.from_wav(audio_path)
#         # Apply compressor effect
#         compressed_audio = audio.compress_dynamic_range(
#             threshold=COMPRESSOR_THRESHOLD,
#             ratio=COMPRESSOR_RATIO,
#             attack=COMPRESSOR_ATTACK,
#             release=COMPRESSOR_RELEASE
#         )
#         # Export compressed audio
#         compressed_audio.export(output_path, format="wav")
#         return True
#     except Exception as e:
#         logging.error(f"Error in compression: {str(e)}")
#         return False

# def process_audio_file(input_path, output_path):
#     """Process a single audio file: noise reduction and compression"""
#     try:
#         # Load audio with librosa
#         audio_data, sample_rate = librosa.load(input_path, sr=None, mono=True)
        
#         # Apply noise reduction
#         denoised_audio = reduce_noise(audio_data, sample_rate)
        
#         # Save temporary denoised file
#         temp_path = output_path + ".temp.wav"
#         ensure_output_directory(temp_path)
#         sf.write(temp_path, denoised_audio, sample_rate)
        
#         # Apply compression
#         ensure_output_directory(output_path)
#         success = apply_compression(temp_path, output_path)
        
#         # Clean up temporary file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
        
#         if success:
#             logging.info(f"Processed: {input_path} -> {output_path}")
#         else:
#             logging.warning(f"Compression failed for {input_path}")
#     except Exception as e:
#         logging.error(f"Error processing {input_path}: {str(e)}")

# def process_dataset():
#     """Process all WAV files in the dataset"""
#     logging.info("Starting noise reduction and compression...")
#     for root, _, files in os.walk(INPUT_ROOT):
#         for file in files:
#             if file.endswith('.wav'):
#                 input_filepath = os.path.join(root, file)
#                 rel_path = Path(input_filepath).relative_to(INPUT_ROOT)
#                 output_filepath = os.path.join(OUTPUT_ROOT, rel_path)
#                 process_audio_file(input_filepath, output_filepath)
#     logging.info("Processing complete.")

# if __name__ == "__main__":
#     process_dataset()

import os
import numpy as np
import soundfile as sf
import librosa
import noisereduce as nr
import pyloudnorm as pyln
from pedalboard import Compressor
from pathlib import Path

def process_audio(input_path, output_path, sr=24000):
    """
    Apply noise reduction and dynamic range compression to an audio file.
    """
    try:
        # Load audio
        y, sr = librosa.load(input_path, sr=sr, mono=True)
        
        # Noise reduction
        # Estimate noise profile from the first 0.5 seconds (assumed to be silence)
        noise_clip = y[:int(0.5 * sr)] if len(y) > int(0.5 * sr) else y
        y_reduced = nr.reduce_noise(y=y, sr=sr, y_noise=noise_clip, prop_decrease=0.8)
        
        # Loudness normalization (ITU-R BS.1770)
        meter = pyln.Meter(sr)  # Create loudness meter
        loudness = meter.integrated_loudness(y_reduced)
        y_normalized = pyln.normalize.loudness(y_reduced, loudness, -23.0)  # Target -23 LUFS
        
        # Dynamic range compression
        compressor = Compressor(
            threshold_db=-16,  # Start compressing above -16 dB
            ratio=4.0,        # 4:1 compression ratio
            attack_ms=1.0,    # Fast attack
            release_ms=100.0  # Moderate release
        )
        y_compressed = compressor(y_normalized, sample_rate=sr)
        
        # Save processed audio
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sf.write(output_path, y_compressed, sr)
        print(f"Processed {output_path}")
    
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def process_dataset(input_dir, output_dir):
    """
    Process the augmented dataset for noise reduction and compression.
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
    
    for aug_type in aug_types:
        for category in categories:
            for subcategory in subcategories:
                input_subdir = os.path.join(input_dir, aug_type, category, subcategory)
                output_subdir = os.path.join(output_dir, aug_type, category, subcategory)
                
                if not os.path.exists(input_subdir):
                    print(f"Skipping {aug_type}/{category}/{subcategory}: Input directory not found")
                    continue
                
                print(f"Processing {aug_type}/{category}/{subcategory}...")
                
                # Get list of audio files
                audio_files = [f for f in os.listdir(input_subdir) if f.endswith('.wav')]
                
                for audio_file in audio_files:
                    input_path = os.path.join(input_subdir, audio_file)
                    output_path = os.path.join(output_subdir, audio_file)
                    process_audio(input_path, output_path)
                    total_files += 1
    
    print(f"Processing completed. Generated {total_files} files in {output_dir}")

def main():
    # Define paths
    input_dir = "Dataset Preparation & Setup/augment_dataset"
    output_dir = "Dataset Preparation & Setup/processed_dataset"
    
    # Expand user home directory
    input_dir = os.path.expanduser(input_dir)
    output_dir = os.path.expanduser(output_dir)
    
    # Remove existing processed dataset to avoid duplicates
    if os.path.exists(output_dir):
        print(f"Removing existing {output_dir}...")
        import shutil
        shutil.rmtree(output_dir)
    
    # Process dataset
    process_dataset(input_dir, output_dir)
    print("Noise reduction and compression completed.")

if __name__ == "__main__":
    main()