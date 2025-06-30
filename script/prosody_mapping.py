
import os
import textgrid
import parselmouth
import numpy as np
from pathlib import Path

def extract_prosody(audio_path, textgrid_path):
    """
    Extract prosodic features (duration, pitch, intensity) from audio and TextGrid.
    Returns a list of words and phonemes with their prosodic attributes.
    """
    try:
        # Load TextGrid
        tg = textgrid.TextGrid.fromFile(textgrid_path)
        
        # Load audio
        snd = parselmouth.Sound(audio_path)
        
        # Extract pitch (F0)
        pitch = snd.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        pitch_times = pitch.xs()
        
        # Extract intensity
        intensity = snd.to_intensity()
        intensity_values = intensity.values[0]
        intensity_times = intensity.xs()
        
        # Get word and phone tiers
        word_tier = next((tier for tier in tg.tiers if tier.name == 'words'), None)
        phone_tier = next((tier for tier in tg.tiers if tier.name == 'phones'), None)
        
        if not word_tier or not phone_tier:
            return None, f"Missing 'words' or 'phones' tier in {textgrid_path}"
        
        # Process prosodic features
        prosody_data = []
        
        for word_interval in word_tier:
            if not word_interval.mark.strip():
                continue  # Skip empty intervals
            word_start = word_interval.minTime
            word_end = word_interval.maxTime
            word_duration = word_end - word_start
            word_text = word_interval.mark.lower()
            
            # Find corresponding phonemes
            phonemes = []
            for phone_interval in phone_tier:
                if phone_interval.minTime >= word_start and phone_interval.maxTime <= word_end:
                    if phone_interval.mark.strip():
                        phone_duration = phone_interval.maxTime - phone_interval.minTime
                        # Get average pitch and intensity for this phoneme
                        phone_time_mid = (phone_interval.minTime + phone_interval.maxTime) / 2
                        pitch_idx = np.argmin(np.abs(pitch_times - phone_time_mid))
                        intensity_idx = np.argmin(np.abs(intensity_times - phone_time_mid))
                        pitch_value = pitch_values[pitch_idx] if pitch_values[pitch_idx] > 0 else None
                        intensity_value = intensity_values[intensity_idx] if intensity_idx < len(intensity_values) else None
                        
                        phonemes.append({
                            'text': phone_interval.mark,
                            'duration': phone_duration,
                            'pitch': pitch_value,
                            'intensity': intensity_value
                        })
            
            # Get average pitch and intensity for the word
            word_time_mid = (word_start + word_end) / 2
            pitch_idx = np.argmin(np.abs(pitch_times - word_time_mid))
            intensity_idx = np.argmin(np.abs(intensity_times - word_time_mid))
            word_pitch = pitch_values[pitch_idx] if pitch_values[pitch_idx] > 0 else None
            word_intensity = intensity_values[intensity_idx] if intensity_idx < len(intensity_values) else None
            
            prosody_data.append({
                'word': word_text,
                'duration': word_duration,
                'pitch': word_pitch,
                'intensity': word_intensity,
                'phonemes': phonemes
            })
        
        return prosody_data, None
    
    except Exception as e:
        return None, f"Error processing {textgrid_path}: {str(e)}"

def generate_annotated_text(prosody_data, output_format='ssml'):
    """
    Generate annotated text with prosody markers.
    Supports SSML-like format or plain text with custom annotations.
    """
    if not prosody_data:
        return ""
    
    if output_format == 'ssml':
        annotated_text = '<speak>'
        for word_data in prosody_data:
            word = word_data['word']
            duration = word_data['duration'] * 1000  # Convert to ms
            pitch = word_data['pitch']
            intensity = word_data['intensity']
            
            # SSML prosody tag
            pitch_str = f' pitch="{pitch:+.0f}Hz"' if pitch else ''
            # Map intensity to volume (rough approximation)
            volume = 'medium' if intensity is None else ('loud' if intensity > 80 else 'soft' if intensity < 60 else 'medium')
            prosody_tag = f'<prosody rate="{duration:.0f}ms" volume="{volume}"{pitch_str}>{word}</prosody>'
            annotated_text += prosody_tag + ' '
        annotated_text += '</speak>'
    else:
        # Custom plain text format (e.g., word|duration_ms|pitch_hz|intensity_db)
        annotated_text = []
        for word_data in prosody_data:
            word = word_data['word']
            duration = word_data['duration'] * 1000  # Convert to ms
            pitch = word_data['pitch'] if word_data['pitch'] else 'N/A'
            intensity = word_data['intensity'] if word_data['intensity'] else 'N/A'
            annotated_text.append(f"{word}|{duration:.0f}|{pitch}|{intensity}")
        annotated_text = '; '.join(annotated_text)
    
    return annotated_text

def process_dataset(audio_dir, textgrid_dir, output_dir, output_format='ssml'):
    """
    Process the dataset to extract prosody and generate annotated text files.
    """
    categories = ['male', 'female']
    subcategories = ['high', 'medium', 'low']
    
    os.makedirs(output_dir, exist_ok=True)
    
    for category in categories:
        for subcategory in subcategories:
            audio_subdir = os.path.join(audio_dir, category, subcategory)
            tg_subdir = os.path.join(textgrid_dir, category, subcategory)
            out_subdir = os.path.join(output_dir, category, subcategory)
            
            if not os.path.exists(audio_subdir) or not os.path.exists(tg_subdir):
                print(f"Skipping {category}/{subcategory}: Directory not found")
                continue
            
            os.makedirs(out_subdir, exist_ok=True)
            print(f"Processing {category}/{subcategory}...")
            
            for tg_file in os.listdir(tg_subdir):
                if tg_file.endswith('.TextGrid'):
                    tg_path = os.path.join(tg_subdir, tg_file)
                    audio_file = tg_file.replace('.TextGrid', '.wav')
                    audio_path = os.path.join(audio_subdir, audio_file)
                    
                    if not os.path.exists(audio_path):
                        print(f"Audio file not found: {audio_path}")
                        continue
                    
                    # Extract prosody
                    prosody_data, error = extract_prosody(audio_path, tg_path)
                    if error:
                        print(error)
                        continue
                    
                    # Generate annotated text
                    annotated_text = generate_annotated_text(prosody_data, output_format)
                    
                    # Save output
                    output_file = os.path.join(out_subdir, tg_file.replace('.TextGrid', f'.{output_format}'))
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(annotated_text)
                    print(f"Generated {output_file}")

def main():
    # Define paths
    # Dataset Preparation & Setup/script/batch_rename.py
    # Dataset Preparation & Setup/TextGrid_Output/
    audio_dir = "Dataset Preparation & Setup/project_voltron_dataset"
    # Dataset Preparation & Setup/TextGrid_Output
    textgrid_dir = "Dataset Preparation & Setup/project_voltron_dataset/TextGrid_Output"
    output_dir = "Dataset Preparation & Setup/project_voltron_dataset/Prosody_Annotated"
    
    # Expand user home directory
    audio_dir = os.path.expanduser(audio_dir)
    textgrid_dir = os.path.expanduser(textgrid_dir)
    output_dir = os.path.expanduser(output_dir)
    
    # Process dataset
    process_dataset(audio_dir, textgrid_dir, output_dir, output_format='ssml')
    print(f"Prosody mapping completed. Annotated files saved in {output_dir}")

if __name__ == "__main__":
    main()