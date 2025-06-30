# import os
# import shutil
# import subprocess
# from pathlib import Path
# from tqdm import tqdm

# def create_aligned_directory_structure(base_path):
#     """Create the Aligned directory structure for male and female."""
#     aligned_path = Path(base_path) / "Aligned"
#     male_path = aligned_path / "male"
#     female_path = aligned_path / "female"
#     intensities = ["low", "medium", "high"]
    
#     # Create Aligned/male directories
#     male_path.mkdir(parents=True, exist_ok=True)
#     for intensity in intensities:
#         (male_path / intensity).mkdir(exist_ok=True)
    
#     # Create Aligned/female directories
#     female_path.mkdir(parents=True, exist_ok=True)
#     for intensity in intensities:
#         (female_path / intensity).mkdir(exist_ok=True)
    
#     return aligned_path

# def prepare_mfa_input(audio_dir, text_dir, mfa_input_dir):
#     """Prepare input files for MFA by copying WAV and TXT files to a flat directory."""
#     mfa_input_dir.mkdir(parents=True, exist_ok=True)
#     file_mapping = {}
    
#     audio_dir = Path(audio_dir)
#     text_dir = Path(text_dir)
    
#     for audio_path in tqdm(audio_dir.rglob("*.wav"), desc="Preparing MFA input"):
#         rel_path = audio_path.parent.relative_to(audio_dir)
#         txt_filename = audio_path.stem + ".txt"
#         txt_path = text_dir / rel_path / txt_filename
        
#         if txt_path.exists():
#             # Create unique filename for MFA (e.g., male_low_Edward_AngerPrimary_1)
#             base_name = f"{audio_dir.name}_{rel_path.name}_{audio_path.stem}"
#             mfa_audio_path = mfa_input_dir / f"{base_name}.wav"
#             mfa_txt_path = mfa_input_dir / f"{base_name}.txt"
            
#             # Copy files
#             shutil.copy2(audio_path, mfa_audio_path)
#             shutil.copy2(txt_path, mfa_txt_path)
            
#             # Store mapping for output
#             file_mapping[base_name] = {
#                 "original_audio": audio_path.name,
#                 "output_dir": rel_path  # Relative path for output (e.g., high, low, medium)
#             }
#         else:
#             print(f"[WARNING] Transcription not found for {audio_path}: {txt_path}")
    
#     return file_mapping



import os
import subprocess
import shutil
from pathlib import Path

def prepare_mfa_input(audio_dir, trans_dir, output_dir):
    """
    Prepare directory structure for MFA by copying audio and transcription files.
    MFA expects audio (.wav) and transcription (.txt) files in the same directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for root, _, files in os.walk(audio_dir):
        for audio_file in files:
            if audio_file.endswith('.wav'):
                # Corresponding transcription file
                trans_file = audio_file.replace('.wav', '.txt')
                trans_path = os.path.join(trans_dir, os.path.relpath(root, audio_dir), trans_file)
                
                if os.path.exists(trans_path):
                    # Copy audio and transcription to output directory
                    dest_audio = os.path.join(output_dir, audio_file)
                    dest_trans = os.path.join(output_dir, trans_file)
                    shutil.copy(os.path.join(root, audio_file), dest_audio)
                    shutil.copy(trans_path, dest_trans)
                else:
                    print(f"Warning: Transcription file {trans_path} not found for {audio_file}")

def run_mfa_alignment(input_dir, output_dir, dictionary_path, acoustic_model_path):
    """
    Run Montreal Forced Aligner to generate .TextGrid files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # MFA align command
    mfa_command = [
        "mfa",
        "align",
        input_dir,
        dictionary_path,
        acoustic_model_path,
        output_dir,
        "--clean",
        "--overwrite",
        "--beam", "10",
        "--retry_beam", "40"
    ]
    
    try:
        result = subprocess.run(mfa_command, check=True, capture_output=True, text=True)
        print(f"MFA alignment completed successfully. Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"MFA alignment failed: {e.stderr}")
        raise

def process_dataset(base_audio_dir, base_trans_dir, output_base_dir, dictionary_path, acoustic_model_path):
    """
    Process the dataset by aligning audio and transcriptions for each category.
    """
    # Define categories (male, female) and subcategories (high, medium, low)
    categories = ['male', 'female']
    subcategories = ['high', 'medium', 'low']
    
    for category in categories:
        for subcategory in subcategories:
            audio_dir = os.path.join(base_audio_dir, category, subcategory)
            trans_dir = os.path.join(base_trans_dir, category, subcategory)
            output_dir = os.path.join(output_base_dir, category, subcategory)
            
            if os.path.exists(audio_dir) and os.path.exists(trans_dir):
                print(f"Processing {category}/{subcategory}...")
                
                # Temporary directory for MFA input
                temp_input_dir = os.path.join(output_base_dir, 'temp_input', category, subcategory)
                prepare_mfa_input(audio_dir, trans_dir, temp_input_dir)
                
                # Run MFA alignment
                run_mfa_alignment(temp_input_dir, output_dir, dictionary_path, acoustic_model_path)
                
                # Clean up temporary directory
                shutil.rmtree(temp_input_dir, ignore_errors=True)
            else:
                print(f"Skipping {category}/{subcategory}: Directory not found.")

def main():
    # Define paths
    

    base_audio_dir = "Dataset Preparation & Setup/project_voltron_dataset"
    base_trans_dir = "Dataset Preparation & Setup/project_voltron_dataset/Transcription"
    output_base_dir = "Dataset Preparation & Setup/project_voltron_dataset/alignments"
    
    # MFA dictionary and acoustic model (update these paths based on your MFA installation)
    dictionary_path = "english_us_arpa"  # Use MFA's pretrained English dictionary
    acoustic_model_path = "english_us_arpa"  # Use MFA's pretrained English acoustic model
    
    # Expand user home directory
    base_audio_dir = os.path.expanduser(base_audio_dir)
    base_trans_dir = os.path.expanduser(base_trans_dir)
    output_base_dir = os.path.expanduser(output_base_dir)
    
    # Process the dataset
    process_dataset(base_audio_dir, base_trans_dir, output_base_dir, dictionary_path, acoustic_model_path)
    print("Phoneme alignment completed. .TextGrid files are saved in", output_base_dir)

if __name__ == "__main__":
    main()
