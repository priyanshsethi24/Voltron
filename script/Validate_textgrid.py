# import os
# import textgrid
# from pathlib import Path
# import difflib

# def load_transcription(trans_path):
#     """Load transcription text from a .txt file."""
#     try:
#         with open(trans_path, 'r', encoding='utf-8') as f:
#             return f.read().strip().lower()
#     except FileNotFoundError:
#         print(f"Transcription file not found: {trans_path}")
#         return None

# def validate_textgrid(textgrid_path, trans_path):
#     """
#     Validate a .TextGrid file for linguistic accuracy.
#     Returns a list of issues found.
#     """
#     issues = []
    
#     try:
#         # Load TextGrid
#         tg = textgrid.TextGrid.fromFile(textgrid_path)
        
#         # Check for required tiers (words and phones)
#         tier_names = [tier.name for tier in tg.tiers]
#         if 'words' not in tier_names:
#             issues.append(f"Missing 'words' tier in {textgrid_path}")
#         if 'phones' not in tier_names:
#             issues.append(f"Missing 'phones' tier in {textgrid_path}")
        
#         # Validate word tier
#         word_tier = next((tier for tier in tg.tiers if tier.name == 'words'), None)
#         if word_tier:
#             word_text = []
#             for interval in word_tier.intervals:
#                 # Check for invalid intervals
#                 if interval.xmin >= interval.xmax:
#                     issues.append(f"Invalid interval in {textgrid_path}: {interval.mark} (xmin={interval.xmin}, xmax={interval.xmax})")
#                 if not interval.mark.strip():
#                     issues.append(f"Empty interval in {textgrid_path}: xmin={interval.xmin}, xmax={interval.xmax}")
#                 word_text.append(interval.mark.lower())
            
#             # Compare with transcription
#             transcription = load_transcription(trans_path)
#             if transcription:
#                 tg_words = ' '.join(word for word in word_text if word).strip()
#                 if tg_words != transcription:
#                     diff = difflib.ndiff(tg_words.split(), transcription.split())
#                     issues.append(f"Transcription mismatch in {textgrid_path}: \nTextGrid: {tg_words}\nTranscription: {transcription}\nDiff: {list(diff)}")
        
#         # Validate phone tier
#         phone_tier = next((tier for tier in tg.tiers if tier.name == 'phones'), None)
#         if phone_tier:
#             for interval in phone_tier.intervals:
#                 if interval.xmin >= interval.xmax:
#                     issues.append(f"Invalid phoneme interval in {textgrid_path}: {interval.mark} (xmin={interval.xmin}, xmax={interval.xmax})")
#                 if not interval.mark.strip():
#                     issues.append(f"Empty phoneme interval in {textgrid_path}: xmin={interval.xmin}, xmax={interval.xmax}")
    
#     except Exception as e:
#         issues.append(f"Error parsing {textgrid_path}: {str(e)}")
    
#     return issues

# def validate_dataset(textgrid_dir, trans_dir):
#     """
#     Validate all .TextGrid files in the dataset.
#     """
#     categories = ['male', 'female']
#     subcategories = ['high', 'medium', 'low']
#     all_issues = []
    
#     for category in categories:
#         for subcategory in subcategories:
#             tg_subdir = os.path.join(textgrid_dir, category, subcategory)
#             trans_subdir = os.path.join(trans_dir, category, subcategory)
            
#             if not os.path.exists(tg_subdir):
#                 all_issues.append(f"TextGrid directory not found: {tg_subdir}")
#                 continue
#             if not os.path.exists(trans_subdir):
#                 all_issues.append(f"Transcription directory not found: {trans_subdir}")
#                 continue
            
#             print(f"Validating {category}/{subcategory}...")
#             for tg_file in os.listdir(tg_subdir):
#                 if tg_file.endswith('.TextGrid'):
#                     tg_path = os.path.join(tg_subdir, tg_file)
#                     trans_file = tg_file.replace('.TextGrid', '.txt')
#                     trans_path = os.path.join(trans_subdir, trans_file)
                    
#                     issues = validate_textgrid(tg_path, trans_path)
#                     if issues:
#                         all_issues.extend(issues)
#                     else:
#                         print(f"{tg_file}: No issues found")
    
#     return all_issues

# def main():
#     # Define paths
#     textgrid_dir = TextGrid_Output"
#     trans_dir = Transcription"
    
#     # Expand user home directory
#     textgrid_dir = os.path.expanduser(textgrid_dir)
#     trans_dir = os.path.expanduser(trans_dir)
    
#     # Validate dataset
#     issues = validate_dataset(textgrid_dir, trans_dir)
    
#     # Report results
#     if issues:
#         print("\nIssues found:")
#         for issue in issues:
#             print(f"- {issue}")
#     else:
#         print("\nNo issues found. All .TextGrid files are valid.")
    
#     print(f"Validation completed. Checked {textgrid_dir}")

# if __name__ == "__main__":
#     main()

import os
import textgrid
from pathlib import Path
import difflib

def load_transcription(trans_path):
    """Load transcription text from a .txt file."""
    try:
        with open(trans_path, 'r', encoding='utf-8') as f:
            return f.read().strip().lower()
    except FileNotFoundError:
        print(f"Transcription file not found: {trans_path}")
        return None

def read_textgrid_raw(textgrid_path):
    """Read raw content of a .TextGrid file for debugging."""
    try:
        with open(textgrid_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading raw file: {str(e)}"

def validate_textgrid(textgrid_path, trans_path):
    """
    Validate a .TextGrid file for linguistic accuracy.
    Returns a list of issues found.
    """
    issues = []
    
    try:
        # Load TextGrid
        tg = textgrid.TextGrid.fromFile(textgrid_path)
        
        # Check for required tiers (words and phones)
        tier_names = [tier.name for tier in tg.tiers]
        if 'words' not in tier_names:
            issues.append(f"Missing 'words' tier in {textgrid_path}")
        if 'phones' not in tier_names:
            issues.append(f"Missing 'phones' tier in {textgrid_path}")
        
        # Validate word tier
        word_tier = next((tier for tier in tg.tiers if tier.name == 'words'), None)
        if word_tier:
            word_text = []
            for interval in word_tier:
                try:
                    # Check for valid interval attributes
                    if not hasattr(interval, 'minTime') or not hasattr(interval, 'maxTime') or not hasattr(interval, 'mark'):
                        issues.append(f"Invalid interval in {textgrid_path}: Missing minTime, maxTime, or mark")
                        continue
                    if interval.minTime >= interval.maxTime:
                        issues.append(f"Invalid interval in {textgrid_path}: {interval.mark} (minTime={interval.minTime}, maxTime={interval.maxTime})")
                    if not interval.mark.strip():
                        issues.append(f"Empty interval in {textgrid_path}: minTime={interval.minTime}, maxTime={interval.maxTime}")
                    word_text.append(interval.mark.lower())
                except AttributeError as e:
                    issues.append(f"Attribute error in {textgrid_path}: {str(e)}")
            
            # Compare with transcription
            transcription = load_transcription(trans_path)
            if transcription:
                tg_words = ' '.join(word for word in word_text if word).strip()
                if tg_words != transcription:
                    diff = difflib.ndiff(tg_words.split(), transcription.split())
                    issues.append(f"Transcription mismatch in {textgrid_path}: \nTextGrid: {tg_words}\nTranscription: {transcription}\nDiff: {list(diff)}")
        
        # Validate phone tier
        phone_tier = next((tier for tier in tg.tiers if tier.name == 'phones'), None)
        if phone_tier:
            for interval in phone_tier:
                try:
                    if not hasattr(interval, 'minTime') or not hasattr(interval, 'maxTime') or not hasattr(interval, 'mark'):
                        issues.append(f"Invalid phoneme interval in {textgrid_path}: Missing minTime, maxTime, or mark")
                        continue
                    if interval.minTime >= interval.maxTime:
                        issues.append(f"Invalid phoneme interval in {textgrid_path}: {interval.mark} (minTime={interval.minTime}, maxTime={interval.maxTime})")
                    if not interval.mark.strip():
                        issues.append(f"Empty phoneme interval in {textgrid_path}: minTime={interval.minTime}, maxTime={interval.maxTime}")
                except AttributeError as e:
                    issues.append(f"Attribute error in {textgrid_path}: {str(e)}")
    
    except Exception as e:
        issues.append(f"Error parsing {textgrid_path}: {str(e)}")
        # Print raw content for debugging
        raw_content = read_textgrid_raw(textgrid_path)
        issues.append(f"Raw content of {textgrid_path}:\n{raw_content[:500]}...")  # Limit to first 500 chars for brevity
    
    return issues

def validate_dataset(textgrid_dir, trans_dir):
    """
    Validate all .TextGrid files in the dataset.
    """
    categories = ['male', 'female']
    subcategories = ['high', 'medium', 'low']
    all_issues = []
    
    for category in categories:
        for subcategory in subcategories:
            tg_subdir = os.path.join(textgrid_dir, category, subcategory)
            trans_subdir = os.path.join(trans_dir, category, subcategory)
            
            if not os.path.exists(tg_subdir):
                all_issues.append(f"TextGrid directory not found: {tg_subdir}")
                continue
            if not os.path.exists(trans_subdir):
                all_issues.append(f"Transcription directory not found: {trans_subdir}")
                continue
            
            print(f"Validating {category}/{subcategory}...")
            for tg_file in os.listdir(tg_subdir):
                if tg_file.endswith('.TextGrid'):
                    tg_path = os.path.join(tg_subdir, tg_file)
                    trans_file = tg_file.replace('.TextGrid', '.txt')
                    trans_path = os.path.join(trans_subdir, trans_file)
                    
                    issues = validate_textgrid(tg_path, trans_path)
                    if issues:
                        all_issues.extend(issues)
                    else:
                        print(f"{tg_file}: No issues found")
    
    return all_issues

def main():
    
    # Define paths
    textgrid_dir = "Dataset Preparation & Setup/TextGrid_Output"
    trans_dir = "Dataset Preparation & Setup/Transcription"
    
    # Expand user home directory
    textgrid_dir = os.path.expanduser(textgrid_dir)
    trans_dir = os.path.expanduser(trans_dir)
    
    # Validate dataset
    issues = validate_dataset(textgrid_dir, trans_dir)
    
    # Report results
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("\nNo issues found. All .TextGrid files are valid.")
    
    print(f"Validation completed. Checked {textgrid_dir}")

if __name__ == "__main__":
    main()