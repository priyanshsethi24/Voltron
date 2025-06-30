import os
from pydub import AudioSegment
import pathlib

# Define paths
INPUT_ROOT = "Dataset Preparation & Setup/project_voltron_dataset"
OUTPUT_ROOT = "Dataset Preparation & Setup/normalized_dataset"
TARGET_DBFS = -1.0  # Target loudness in dBFS (decibels full scale)

def ensure_output_directory(output_path):
    """Create output directory if it doesn't exist"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

def normalize_audio(input_path, output_path):
    """Normalize audio file to target dBFS and save to output path"""
    try:
        # Load audio file
        audio = AudioSegment.from_wav(input_path)
        
        # Calculate the change needed to reach target dBFS
        change_in_dbfs = TARGET_DBFS - audio.dBFS
        
        # Apply gain to normalize
        normalized_audio = audio.apply_gain(change_in_dbfs)
        
        # Ensure output directory exists
        ensure_output_directory(output_path)
        
        # Export normalized audio
        normalized_audio.export(output_path, format="wav")
        print(f"Normalized: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def process_dataset():
    """Process all WAV files in the dataset"""
    # Walk through input dataset
    for root, _, files in os.walk(INPUT_ROOT):
        for file in files:
            if file.endswith('.wav'):
                # Input file path
                input_filepath = os.path.join(root, file)
                
                # Construct output file path, maintaining directory structure
                rel_path = pathlib.Path(input_filepath).relative_to(INPUT_ROOT)
                output_filepath = os.path.join(OUTPUT_ROOT, rel_path)
                
                # Normalize and save
                normalize_audio(input_filepath, output_filepath)

if __name__ == "__main__":
    process_dataset()