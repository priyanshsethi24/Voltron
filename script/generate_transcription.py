
import os
import whisper
from pathlib import Path

def create_transcription_directory_structure(base_path):
    """Create the Transcription directory structure for male and female."""
    transcription_path = Path(base_path) / "project_voltron_dataset/alignments"
    male_path = transcription_path / "male"
    female_path = transcription_path / "female"
    intensities = ["low", "medium", "high"]
    
    # Create Transcription/male directories
    male_path.mkdir(parents=True, exist_ok=True)
    for intensity in intensities:
        (male_path / intensity).mkdir(exist_ok=True)
    
    # Create Transcription/female directories
    female_path.mkdir(parents=True, exist_ok=True)
    for intensity in intensities:
        (female_path / intensity).mkdir(exist_ok=True)
    
    return transcription_path

def generate_transcription(audio_path, model):
    """Generate transcription for an audio file using Whisper."""
    try:
        result = model.transcribe(str(audio_path))
        transcription = result["text"].strip()
        if not transcription:
            print(f"[WARNING] Empty transcription for {audio_path}")
            return None
        return transcription
    except Exception as e:
        print(f"[ERROR] Failed to transcribe {audio_path}: {e}")
        return None

def process_audio_files(input_dir, output_dir, model):
    """Process all WAV files and generate transcriptions."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    for audio_path in input_dir.rglob("*.wav"):
        rel_path = audio_path.parent.relative_to(input_dir)
        output_root = output_dir / rel_path
        output_root.mkdir(parents=True, exist_ok=True)
        
        txt_filename = audio_path.stem + ".txt"
        output_path = output_root / txt_filename
        
        # Generate transcription
        transcription = generate_transcription(audio_path, model)
        if transcription:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcription)
            print(f"[SUCCESS] Generated transcription for {audio_path} at {output_path}")
        else:
            print(f"[SKIP] Skipped {audio_path} due to transcription error")

def main():
    # Define base paths
    
    base_path = Path.home() / "AI_Voice_Assistent_Project/Dataset Preparation & Setup"
    print(Path.home())


    audio_dataset_path = base_path / "project_voltron_dataset"
    
    # Verify audio dataset exists
    if not audio_dataset_path.exists():
        print(f"[ERROR] Audio dataset directory not found: {audio_dataset_path}")
        return
    
    # Create Transcription directory structure
    print("[INFO] Creating Transcription directory structure...")
    transcription_path = create_transcription_directory_structure(base_path)
    
    # Load Whisper model
    print("[INFO] Loading Whisper model...")
    model = whisper.load_model("base")  # Use 'small' or 'medium' for better accuracy if needed
    
    # Process male audio files
    male_input = audio_dataset_path / "male"
    male_output = transcription_path / "male"
    if male_input.exists():
        print("[INFO] Processing male audio files...")
        process_audio_files(male_input, male_output, model)
    else:
        print(f"[WARNING] Male directory not found: {male_input}")
    
    # Process female audio files
    female_input = audio_dataset_path / "female"
    female_output = transcription_path / "female"
    if female_input.exists():
        print("[INFO] Processing female audio files...")
        process_audio_files(female_input, female_output, model)
    else:
        print(f"[WARNING] Female directory not found: {female_input}")
    
    print("[INFO] Transcription generation completed.")

if __name__ == "__main__":
    main()