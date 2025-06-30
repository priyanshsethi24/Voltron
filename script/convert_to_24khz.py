# import os
# import shutil
# import librosa
# from pydub import AudioSegment
# import tempfile

# def check_and_convert_to_24khz(input_path, output_path):
#     """Check sampling rate and convert WAV file to 24kHz if necessary."""
#     # Check sampling rate with librosa
#     try:
#         sr = librosa.get_samplerate(input_path)
#         if sr == 24000:
#             print(f"{input_path} is already 24kHz, copying to {output_path}")
#             shutil.copy2(input_path, output_path)
#             return
#     except Exception as e:
#         print(f"Error checking sampling rate for {input_path}: {e}")
#         return

#     # Convert to 24kHz using pydub
#     try:
#         audio = AudioSegment.from_wav(input_path)
#         audio = audio.set_frame_rate(24000)
#         audio.export(output_path, format="wav")
#         print(f"Converted {input_path} to 24kHz at {output_path}")
#     except Exception as e:
#         print(f"Error converting {input_path} to 24kHz: {e}")

# def process_directory(input_dir, output_dir):
#     """Process all WAV files in the input directory and its subdirectories."""
#     os.makedirs(output_dir, exist_ok=True)
    
#     for root, dirs, files in os.walk(input_dir):
#         # Create corresponding output directory structure
#         rel_path = os.path.relpath(root, input_dir)
#         output_root = os.path.join(output_dir, rel_path)
#         os.makedirs(output_root, exist_ok=True)
        
#         # Process WAV files
#         for file in files:
#             if file.endswith(".wav"):
#                 input_path = os.path.join(root, file)
#                 output_path = os.path.join(output_root, file)
#                 check_and_convert_to_24khz(input_path, output_path)

# def main():
#     # Define base paths
#     base_path = os.path.expanduser("Dataset Preparation & Setup/project_voltron_dataset")
#     temp_dir = os.path.join(base_path, "temp")
    
#     # Create temporary directory for processing
#     os.makedirs(temp_dir, exist_ok=True)
    
#     # Process male directory
#     male_input = os.path.join(base_path, "male")
#     male_output = os.path.join(temp_dir, "male")
#     if os.path.exists(male_input):
#         process_directory(male_input, male_output)
    
#     # Copy empty female directory structure
#     female_input = os.path.join(base_path, "female")
#     female_output = os.path.join(temp_dir, "female")
#     if os.path.exists(female_input):
#         shutil.copytree(female_input, female_output, dirs_exist_ok=True)
#         print(f"Copied empty female directory structure to {female_output}")
    
#     # Replace original directory with processed one
#     shutil.rmtree(base_path + "/male", ignore_errors=True)
#     shutil.rmtree(base_path + "/female", ignore_errors=True)
#     if os.path.exists(male_output):
#         shutil.move(male_output, os.path.join(base_path, "male"))
#     if os.path.exists(female_output):
#         shutil.move(female_output, os.path.join(base_path, "female"))
    
#     # Clean up temporary directory
#     shutil.rmtree(temp_dir, ignore_errors=True)
#     print("Conversion to 24kHz completed.")

# if __name__ == "__main__":
#     main()

import os
import shutil
import librosa
from pydub import AudioSegment

def check_and_convert_to_24khz(input_path, output_path):
    """Check sampling rate and convert WAV file to 24kHz if necessary."""
    try:
        sr = librosa.get_samplerate(input_path)
        if sr == 24000:
            print(f"[COPY] {input_path} is already 24kHz, copying to {output_path}")
            shutil.copy2(input_path, output_path)
            return
    except Exception as e:
        print(f"[ERROR] Checking sampling rate for {input_path}: {e}")
        return

    try:
        audio = AudioSegment.from_wav(input_path)
        audio = audio.set_frame_rate(24000)
        audio.export(output_path, format="wav")
        print(f"[CONVERTED] {input_path} -> {output_path}")
    except Exception as e:
        print(f"[ERROR] Converting {input_path} to 24kHz: {e}")

def process_directory(input_dir, output_dir):
    """Recursively process all WAV files in the input directory."""
    for root, dirs, files in os.walk(input_dir):
        rel_path = os.path.relpath(root, input_dir)
        output_root = os.path.join(output_dir, rel_path)
        os.makedirs(output_root, exist_ok=True)

        for file in files:
            if file.lower().endswith(".wav"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_root, file)
                check_and_convert_to_24khz(input_path, output_path)

def main():
    base_path = os.path.expanduser("../Dataset Preparation & Setup/project_voltron_dataset")
    temp_dir = os.path.join(base_path, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Process both male and female directories
    for gender in ["male", "female"]:
        input_dir = os.path.join(base_path, gender)
        output_dir = os.path.join(temp_dir, gender)

        if os.path.exists(input_dir):
            print(f"Processing {gender} directory...")
            process_directory(input_dir, output_dir)

    # Replace original directories with processed ones
    for gender in ["male", "female"]:
        original_dir = os.path.join(base_path, gender)
        processed_dir = os.path.join(temp_dir, gender)

        shutil.rmtree(original_dir, ignore_errors=True)
        if os.path.exists(processed_dir):
            shutil.move(processed_dir, original_dir)

    shutil.rmtree(temp_dir, ignore_errors=True)
    print("\n✅ All files converted to 24kHz.")

if __name__ == "__main__":
    main()
