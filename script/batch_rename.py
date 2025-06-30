import os
import re

def rename_takes(root_path):
    for speaker in os.listdir(root_path):
        speaker_path = os.path.join(root_path, speaker)
        if not os.path.isdir(speaker_path):
            continue

        # Dictionary to group takes by their base emotion string
        take_groups = {}

        for filename in os.listdir(speaker_path):
            file_path = os.path.join(speaker_path, filename)

            # Match filenames with the pattern: male_AngerPrimary_High_TakeX.wav
            match = re.match(r'^(.*)_Take(\d+)\.wav$', filename)
            if match:
                base_name = match.group(1)
                if base_name not in take_groups:
                    take_groups[base_name] = []
                take_groups[base_name].append((int(match.group(2)), filename))

        # Rename files in each group
        for base_name, takes in take_groups.items():
            # Sort by the original Take number
            sorted_takes = sorted(takes, key=lambda x: x[0])
            for index, (_, old_filename) in enumerate(sorted_takes, start=1):
                new_filename = f"{base_name}_{index}.wav"
                old_path = os.path.join(speaker_path, old_filename)
                new_path = os.path.join(speaker_path, new_filename)
                print(f"Renaming: {old_filename} -> {new_filename}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    dataset_path = "Dataset Preparation & Setup/Dataset"
    rename_takes(dataset_path)
