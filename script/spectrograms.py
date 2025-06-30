import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
# from pathlib import Path

def generate_spectrogram(audio_path, output_path):
    """Generate a spectrogram PNG for an audio file."""
    try:
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        plt.figure(figsize=(10, 4))
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz')
        plt.colorbar(format='%+2.0f dB')
        plt.title(os.path.basename(audio_path))
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        print(f"Generated spectrogram: {output_path}")
    except Exception as e:
        print(f"Error generating spectrogram for {audio_path}: {str(e)}")

def generate_spectrograms(input_dir, output_dir, max_files=50):
    """
    Generate spectrograms for up to max_files WAV files.
    """
    aug_types = [
        'pitch_up', 'pitch_down', 'tempo_fast', 'tempo_slow',
        'intensity_louder', 'intensity_quieter'
    ]
    categories = ['male','female']  # Adjust if female data is added
    subcategories = ['high', 'medium', 'low']
    file_count = 0
    
    for aug_type in aug_types:
        for category in categories:
            for subcategory in subcategories:
                subdir = os.path.join(input_dir, aug_type, category, subcategory)
                if not os.path.exists(subdir):
                    continue
                
                print(f"Processing spectrograms in {aug_type}/{category}/{subcategory}...")
                for audio_file in os.listdir(subdir):
                    if file_count >= max_files:
                        return
                    if audio_file.endswith('.wav'):
                        audio_path = os.path.join(subdir, audio_file)
                        output_path = os.path.join(
                            output_dir, aug_type, category, subcategory,
                            audio_file.replace('.wav', '.png')
                        )
                        generate_spectrogram(audio_path, output_path)
                        file_count += 1
    
    print(f"Spectrogram generation completed. Generated {file_count} PNGs in {output_dir}")

def main():

    input_dir = "Dataset Preparation & Setup/normalized_dataset"
    output_dir = "Dataset Preparation & Setup/quality_checks/spectrograms"
    
    input_dir = os.path.expanduser(input_dir)
    output_dir = os.path.expanduser(output_dir)
    
    generate_spectrograms(input_dir, output_dir, max_files=50)
    print("Spectrogram canary completed. Inspect PNGs for anomalies.")

if __name__ == "__main__":
    main()
