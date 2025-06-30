# from pydub import AudioSegment

# # Load audio file (WAV, MP3, etc.)


# audio = AudioSegment.from_file("Edward_AngerPrimary_1.wav")

# # 🔊 Peak loudness in dBFS (max amplitude)
# peak_dbfs = audio.max_dBFS

# # 🔊 Average loudness in dBFS (based on RMS)
# average_dbfs = audio.dBFS

# print(f"Peak dBFS: {peak_dbfs:.2f} dB")
# print(f"Average dBFS (RMS): {average_dbfs:.2f} dB")

# import os
# from pydub import AudioSegment

# # Path to your normalized dataset root
# root_dir = "normalized_dataset"

# # Walk through all subdirectories
# for subdir, _, files in os.walk(root_dir):
#     for file in files:
#         if file.lower().endswith(".wav"):
#             file_path = os.path.join(subdir, file)
            
#             try:
#                 audio = AudioSegment.from_file(file_path)

#                 # Peak and average dBFS
#                 peak_dbfs = audio.max_dBFS
#                 average_dbfs = audio.dBFS

#                 # Minimum sample value (raw audio values)
#                 raw_samples = audio.get_array_of_samples()
#                 min_sample = min(raw_samples)

#                 print(f"File: {file_path}")
#                 print(f"  Peak dBFS   : {peak_dbfs:.2f} dB")
#                 print(f"  Average dBFS: {average_dbfs:.2f} dB")
#                 print(f"  Min Sample Val: {min_sample}")
#                 print("-" * 40)

#             except Exception as e:
#                 print(f"Error processing {file_path}: {e}")

# import os
# import math
# from pydub import AudioSegment

# # Path to root normalized dataset folder
# root_dir = "normalized_dataset"

# # Acceptable RMS amplitude range
# rms_min_threshold = 0.01
# rms_max_threshold = 0.1

# def calculate_rms(audio):
#     samples = audio.get_array_of_samples()
#     squared = [(sample / (2 ** (8 * audio.sample_width - 1))) ** 2 for sample in samples]
#     return math.sqrt(sum(squared) / len(squared))

# # Traverse male and female folders
# for gender in ["male", "female"]:
#     gender_path = os.path.join(root_dir, gender)
#     for subdir, _, files in os.walk(gender_path):
#         for file in files:
#             if file.lower().endswith(".wav"):
#                 file_path = os.path.join(subdir, file)
#                 try:
#                     audio = AudioSegment.from_file(file_path)
#                     rms_amplitude = calculate_rms(audio)

#                     if rms_amplitude < rms_min_threshold or rms_amplitude > rms_max_threshold:
#                         print(f"\nUnusual RMS in: {file_path}")
#                         print(f"  RMS amplitude: {rms_amplitude:.5f}")
#                 except Exception as e:
#                     print(f"Error reading {file_path}: {e}")


import os
import librosa
import numpy as np
from pathlib import Path

def calculate_rms(audio_path):
    """Calculate RMS amplitude of an audio file."""
    try:
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        rms = np.sqrt(np.mean(y**2))
        return rms
    except Exception as e:
        return None, f"Error processing {audio_path}: {str(e)}"

def check_rms(input_dir, output_file):
    """
    Check RMS amplitude for all WAV files and flag unusual values (outside 0.01–0.1).
    Save results to output_file.
    """
    issues = []
    aug_types = [
        'pitch_up', 'pitch_down', 'tempo_fast', 'tempo_slow',
        'intensity_louder', 'intensity_quieter'
    ]
    categories = ['male']  # Adjust if female data is added
    subcategories = ['high', 'medium', 'low']
    
    for aug_type in aug_types:
        for category in categories:
            for subcategory in subcategories:
                subdir = os.path.join(input_dir, aug_type, category, subcategory)
                if not os.path.exists(subdir):
                    continue
                
                print(f"Checking RMS in {aug_type}/{category}/{subcategory}...")
                for audio_file in os.listdir(subdir):
                    if audio_file.endswith('.wav'):
                        audio_path = os.path.join(subdir, audio_file)
                        rms = calculate_rms(audio_path)
                        if isinstance(rms, tuple):  # Error case
                            issues.append(rms[1])
                            continue
                        if rms < 0.01 or rms > 0.1:
                            issues.append(f"{audio_path} unusual RMS: {rms:.6f}")
    
    # Save issues to output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        if issues:
            f.write("RMS Issues:\n")
            for issue in issues:
                f.write(f"- {issue}\n")
        else:
            f.write("No RMS issues found.\n")
    
    print(f"RMS check completed. Results saved to {output_file}")
    return issues

def main():
    input_dir = "Dataset Preparation & Setup/project_voltron_dataset"
    output_file = "/Dataset Preparation & Setup/quality_checks/rms_issues.txt"
    
    input_dir = os.path.expanduser(input_dir)
    output_file = os.path.expanduser(output_file)
    
    issues = check_rms(input_dir, output_file)
    if issues:
        print("Issues found. Check", output_file)
    else:
        print("All files passed RMS check.")

if __name__ == "__main__":
    main()

