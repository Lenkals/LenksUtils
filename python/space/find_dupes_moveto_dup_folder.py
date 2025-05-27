import os
import subprocess
import sys
import shutil
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime

def get_cksum(file_path):
    try:
        result = subprocess.run(['cksum', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            checksum, size, _ = result.stdout.strip().split(maxsplit=2)
            return int(checksum), int(size)
    except Exception:
        pass
    return None, None

def get_file_date(file_path):
    """Return file date as YYYYMMDD from creation or modification timestamp."""
    try:
        timestamp = os.path.getctime(file_path)
    except AttributeError:
        timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).strftime('%Y%m%d')

def find_duplicates_cksum(root_dir):
    file_list = []
    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(foldername, filename)
            if os.path.isfile(full_path):
                file_list.append(full_path)

    checksum_map = defaultdict(list)
    reclaimable = 0

    print(f"\n🔍 Scanning {len(file_list)} files...\n")
    for file_path in tqdm(file_list, desc="Calculating checksums", unit="file"):
        checksum, size = get_cksum(file_path)
        if checksum is not None:
            key = (checksum, size)
            checksum_map[key].append(file_path)

    duplicates = {k: v for k, v in checksum_map.items() if len(v) > 1}
    for (_, size), files in duplicates.items():
        reclaimable += size * (len(files) - 1)

    return duplicates, reclaimable

def bytes_to_readable(num_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} PB"

def move_duplicates(duplicates, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    for (_, _), files in tqdm(duplicates.items(), desc="Moving duplicates", unit="group"):
        original = files[0]
        for idx, dup_file in enumerate(files[1:], start=1):
            base_name = os.path.basename(dup_file)
            date_str = get_file_date(dup_file)
            name, ext = os.path.splitext(base_name)
            new_name = f"{date_str}_{name}_{idx}{ext}"
            target_path = os.path.join(target_folder, new_name)

            try:
                shutil.move(dup_file, target_path)
            except Exception as e:
                print(f"❌ Failed to move {dup_file} -> {target_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_duplicates.py /path/to/folder")
        sys.exit(1)

    folder_to_scan = sys.argv[1]
    if not os.path.isdir(folder_to_scan):
        print(f"Error: '{folder_to_scan}' is not a valid directory.")
        sys.exit(1)

    print(f"\n📁 Finding duplicates in: '{folder_to_scan}'")
    duplicates, reclaimable = find_duplicates_cksum(folder_to_scan)

    print(f"\n🔁 Duplicate file groups found: {len(duplicates)}")
    print(f"💾 Reclaimable space: {bytes_to_readable(reclaimable)}")

    for (_, size), files in duplicates.items():
        print("\n📁 Duplicate Group:")
        print(f"  ✅ Original: {files[0]}")
        for f in files[1:]:
            print(f"  ❌ Duplicate: {f}")

    # Move duplicates
    move_folder = os.path.join(folder_to_scan, "duplicate_files_collected")
    move_duplicates(duplicates, move_folder)
    print(f"\n🚚 All duplicates moved to: {move_folder}")
