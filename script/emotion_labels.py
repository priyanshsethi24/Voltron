# import fitz  # PyMuPDF
# import re
# import json

# def extract_emotion_metadata(pdf_path):
#     doc = fitz.open(pdf_path)
#     emotion_data = {}

#     emotion_name_pattern = re.compile(r"^\d+\.\s*(.+?)\s*$")
#     category_pattern = re.compile(r"Category:\s*(.+?)\s*(\(|$)")
#     description_pattern = re.compile(r"Scenario: (.+)")

#     current_emotion = None
#     current_category = None
#     description_buffer = ""

#     for page in doc:
#         text = page.get_text().split("\n")
#         for line in text:
#             line = line.strip()

#             # Detect emotion name
#             match = emotion_name_pattern.match(line)
#             if match:
#                 if current_emotion and description_buffer:
#                     # Save the previous emotion entry
#                     key = f"{current_emotion}{'Primary' if 'Primary' in current_category else 'Secondary'}"
#                     emotion_data[key] = {"description": description_buffer.strip()}

#                 current_emotion = match.group(1).strip().replace(" ", "")
#                 current_category = None
#                 description_buffer = ""
#                 continue

#             # Detect category
#             match = category_pattern.search(line)
#             if match:
#                 current_category = match.group(1).strip()
#                 continue

#             # Detect description line
#             match = description_pattern.search(line)
#             if match:
#                 description_buffer = match.group(1).strip()
#                 continue

#     # Save the last entry
#     if current_emotion and description_buffer:
#         key = f"{current_emotion}{'Primary' if 'Primary' in current_category else 'Secondary'}"
#         emotion_data[key] = {"description": description_buffer.strip()}

#     return emotion_data


# # Run the function and export to JSON
# metadata = extract_emotion_metadata("Emotional Recordings For PJV - Sentences (Kundan).pdf")

# # Save as JSON
# with open("emotion_metadata.json", "w", encoding="utf-8") as f:
#     json.dump(metadata, f, indent=4, ensure_ascii=False)

# print(f"Extracted {len(metadata)} emotion descriptions.")

# import re
# import json

# def extract_emotions_with_description(text_path):
#     with open(text_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     metadata = {}
#     current_emotion = None
#     description_buffer = ""
#     capture = False

#     for line in lines:
#         line = line.strip()

#         # Detect new emotion title (e.g. "101. Tech Nostalgia" or just "Tech Nostalgia")
#         title_match = re.match(r'^(\d+\.\s*)?([A-Za-z][A-Za-z\s\-\(\)]+)$', line)
#         if title_match:
#             # Save previous
#             if current_emotion and description_buffer:
#                 metadata[current_emotion] = {"description": description_buffer.strip()}
#             current_emotion = title_match.group(2).strip().replace(" ", "").replace("(", "").replace(")", "")
#             description_buffer = ""
#             capture = False
#             continue

#         # Detect "Description:" line
#         if line.lower().startswith("description:"):
#             description_buffer = line.split(":", 1)[1].strip()
#             capture = True
#             continue

#         # Continue collecting multi-line description
#         if capture and line and not line.lower().startswith("example sentence"):
#             description_buffer += " " + line

#     # Save last one
#     if current_emotion and description_buffer:
#         metadata[current_emotion] = {"description": description_buffer.strip()}

#     return metadata


# # Example usage
# text_path = "emotions1.txt"  # Make sure this is the plain text version from the PDF
# emotions = extract_emotions_with_description(text_path)

# # Save to JSON
# with open("emotions_with_descriptions.json", "w", encoding="utf-8") as f:
#     json.dump(emotions, f, indent=4, ensure_ascii=False)

# print(f"✅ Extracted {len(emotions)} emotions with descriptions.")

# import json
# import re

# def parse_emotion_file(txt_file_path, json_output_path):
#     with open(txt_file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     emotions = {}
#     current_emotion = {}
#     name = category = description = None

#     for line in lines:
#         line = line.strip()

#         if re.match(r'^\d+\.', line):  # Match number and emotion name like "2. Relief"
#             if name and description:  # Save previous entry before starting new one
#                 key = name + category if category else name
#                 emotions[key] = {"description": description}
#                 category = description = None

#             name = line.split('. ', 1)[1]

#         elif line.startswith("Category:"):
#             category = line.replace("Category:", "").strip().replace(" ", "") or None

#         elif line.startswith("Description:"):
#             description = line.replace("Description:", "").strip()

#     # Save the last emotion
#     if name and description:
#         key = name + category if category else name
#         emotions[key] = {"description": description}

#     # Write to JSON
#     with open(json_output_path, 'w', encoding='utf-8') as json_file:
#         json.dump(emotions, json_file, ensure_ascii=False, indent=2)

#     print(f"✅ JSON file created at: {json_output_path}")

# # Example usage
# parse_emotion_file('emotions.txt', 'emotions_labels.json')

# import re
# import json

# def extract_emotions_with_description(text_path):
#     with open(text_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     metadata = {}
#     current_emotion = None
#     current_category = ""
#     description_buffer = ""
#     capture_description = False

#     for line in lines:
#         line = line.strip()

#         # Match titles like "141. Relief" or just "Relief"
#         title_match = re.match(r'^(\d+\.\s*)?([A-Za-z][A-Za-z\s\-\(\)]+)$', line)
#         if title_match:
#             # Save the last emotion if description exists
#             if current_emotion and description_buffer:
#                 key = current_emotion + current_category if current_category else current_emotion
#                 metadata[key] = {"description": description_buffer.strip()}

#             # Start new emotion
#             current_emotion = title_match.group(2).strip().replace(" ", "").replace("(", "").replace(")", "")
#             current_category = ""
#             description_buffer = ""
#             capture_description = False
#             continue

#         # Detect "Category:"
#         if line.lower().startswith("category:"):
#             cat = line.split(":", 1)[1].strip()
#             current_category = cat.split()[0] if cat else ""
#             continue

#         # Detect "Description:"
#         if line.lower().startswith("description:"):
#             description_buffer = line.split(":", 1)[1].strip()
#             capture_description = True
#             continue

#         # Continue capturing multiline description
#         if capture_description and line and not line.lower().startswith("example sentence"):
#             description_buffer += " " + line

#     # Save the last emotion
#     if current_emotion and description_buffer:
#         key = current_emotion + current_category if current_category else current_emotion
#         metadata[key] = {"description": description_buffer.strip()}

#     return metadata


# # Example usage
# text_path = "emotions1.txt"  # Your input .txt file
# output_path = "emotions_with_descriptions.json"

# emotions = extract_emotions_with_description(text_path)

# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump(emotions, f, indent=4, ensure_ascii=False)

# print(f"✅ Extracted {len(emotions)} emotions and saved to {output_path}")

import re
import json

def extract_emotions_with_description(text_path):
    with open(text_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    emotions_list = []
    current_emotion = None
    current_category = ""
    description_buffer = ""
    capture_description = False

    for line in lines:
        line = line.strip()

        # Match titles like "141. Relief" or just "Relief"
        title_match = re.match(r'^(\d+\.\s*)?([A-Za-z][A-Za-z\s\-\(\)]+)$', line)
        if title_match:
            # Save the last emotion if description exists
            if current_emotion and description_buffer:
                key = current_emotion + current_category if current_category else current_emotion
                emotions_list.append({
                    key: {"description": description_buffer.strip()}
                })

            # Start new emotion
            current_emotion = title_match.group(2).strip().replace(" ", "").replace("(", "").replace(")", "")
            current_category = ""
            description_buffer = ""
            capture_description = False
            continue

        # Detect "Category:"
        if line.lower().startswith("category:"):
            cat = line.split(":", 1)[1].strip()
            current_category = cat.split()[0] if cat else ""
            continue

        # Detect "Description:"
        if line.lower().startswith("description:"):
            description_buffer = line.split(":", 1)[1].strip()
            capture_description = True
            continue

        # Continue capturing multiline description
        if capture_description and line and not line.lower().startswith("example sentence"):
            description_buffer += " " + line

    # Save the last one
    if current_emotion and description_buffer:
        key = current_emotion + current_category if current_category else current_emotion
        emotions_list.append({
            key: {"description": description_buffer.strip()}
        })

    return emotions_list


# Example usage
text_path = "emotions1.txt"  # Your input .txt file
output_path = "emotions_with_descriptions.json"

emotions = extract_emotions_with_description(text_path)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(emotions, f, indent=4, ensure_ascii=False)

print(f"✅ Extracted {len(emotions)} emotion entries (including duplicates) and saved to {output_path}")


# import json
# import re

# def append_emotion_to_description(input_path, output_path):
#     # Load the existing emotion descriptions
#     with open(input_path, "r", encoding="utf-8") as f:
#         emotion_entries = json.load(f)

#     updated_emotions = []

#     for entry in emotion_entries:
#         for key, value in entry.items():
#             # Remove trailing dot from the description if present
#             description = value.get("description", "").strip()
#             if description.endswith("."):
#                 description = description[:-1].strip()

#             # Match if the key ends with Primary or Secondary
#             match = re.match(r"^([A-Z][a-zA-Z]+)(Primary|Secondary)$", key)
#             if match:
#                 emotion_part = match.group(1).lower()
#             else:
#                 # Otherwise just use the full key as lowercase
#                 emotion_part = key[0].lower() + key[1:]

#             # Append the emotion and period
#             updated_description = f"{description} {emotion_part}."
#             updated_emotions.append({
#                 key: {
#                     "description": updated_description
#                 }
#             })

#     # Save updated entries
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(updated_emotions, f, indent=4, ensure_ascii=False)

#     print(f"✅ Appended emotion keywords to {len(updated_emotions)} entries and saved to {output_path}")


# # Example usage
# input_json_path = "emotions_with_descriptions.json"
# output_json_path = "emotion_labels.json"

# append_emotion_to_description(input_json_path, output_json_path)


import json
import re

def append_emotion_to_description(input_path, output_path):
    # Load the existing emotion descriptions
    with open(input_path, "r", encoding="utf-8") as f:
        emotion_entries = json.load(f)

    updated_emotions = []

    for entry in emotion_entries:
        for key, value in entry.items():
            # Get original description and strip whitespace
            description = value.get("description", "").strip()

            # Remove trailing period (if any)
            if description.endswith("."):
                description = description[:-1].strip()

            # Detect if key includes Primary or Secondary category
            match = re.match(r"^([A-Z][a-zA-Z]+)(Primary|Secondary)$", key)
            if match:
                emotion_part = match.group(1).lower()
            else:
                # If no category, use key as camelCase
                emotion_part = key[0].lower() + key[1:]

            # Append a space and the emotion_part (if not already present), then a period
            updated_description = f"{description} {emotion_part}."

            # Normalize spacing before saving
            updated_description = re.sub(r'\s+', ' ', updated_description).strip()

            updated_emotions.append({
                key: {
                    "description": updated_description
                }
            })

    # Save updated JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(updated_emotions, f, indent=4, ensure_ascii=False)

    print(f"✅ Appended emotion keywords to {len(updated_emotions)} entries and saved to {output_path}")


# Example usage
input_json_path = "emotions_with_descriptions.json"
output_json_path = "emotion_labels.json"

append_emotion_to_description(input_json_path, output_json_path)



