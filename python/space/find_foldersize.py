import os
import sys
from tqdm import tqdm

def get_folder_size(path):
    """Calculate total size of a folder recursively (including all files and subfolders)."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total += os.path.getsize(fp)
            except:
                continue  # Skip unreadable files
    return total

def bytes_to_readable(num_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} PB"

def get_subfolder_sizes(root_path):
    subfolders = [entry for entry in os.scandir(root_path) if entry.is_dir(follow_symlinks=False)]
    folder_sizes = []

    print(f"🔍 Scanning {len(subfolders)} subfolders...\n")
    for entry in tqdm(subfolders, desc="Calculating sizes", unit="folder"):
        folder_path = entry.path
        size = get_folder_size(folder_path)
        folder_sizes.append((folder_path, size))

    return sorted(folder_sizes, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python folder_sizes.py /path/to/root_folder")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Error: {root} is not a valid folder.")
        sys.exit(1)

    sizes = get_subfolder_sizes(root)

    print("\n📂 Folder sizes (sorted by usage):\n")
    for path, size in sizes:
        print(f"{bytes_to_readable(size)}\t{path}")
