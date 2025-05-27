import os
import subprocess
import sys
from collections import defaultdict
from tqdm import tqdm

def get_cksum(file_path):
    """Get CRC checksum and size using the `cksum` command."""
    try:
        result = subprocess.run(['cksum', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            checksum, size, _ = result.stdout.strip().split(maxsplit=2)
            return int(checksum), int(size)
        else:
            return None, None
    except Exception as e:
        return None, None

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_duplicates.py /path/to/folder")
        sys.exit(1)

    folder_to_scan = sys.argv[1]
    if not os.path.isdir(folder_to_scan):
        print(f"Error: '{folder_to_scan}' is not a valid directory.")
        sys.exit(1)

    print(f"Findig dupes in this folder '{folder_to_scan}' ")
    duplicates, reclaimable = find_duplicates_cksum(folder_to_scan)

    print(f"\n🔁 Duplicate file groups found: {len(duplicates)}")
    print(f"💾 Reclaimable space: {bytes_to_readable(reclaimable)}")

    for (_, size), files in duplicates.items():
        print("\n📁 Duplicate Group:")
        print(f"  ✅ Original: {files[0]}")
        for f in files[1:]:
            print(f"  ❌ Duplicate: {f}")
