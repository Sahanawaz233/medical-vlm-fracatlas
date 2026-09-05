import os
import sys
import urllib.request
import zipfile

def progress_callback(block_num, block_size, total_size):
    downloaded = block_num * block_size
    percent = min(100, int(downloaded * 100 / total_size))
    # Standard output flush for progress bar
    sys.stdout.write(f"\rDownloading FracAtlas dataset: {percent}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)")
    sys.stdout.flush()

def main():
    print("=================================================================")
    print("                FracAtlas Auto-Downloader Script                 ")
    print("=================================================================")
    
    # 1. Setup directories
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    
    zip_path = os.path.join(raw_dir, "FracAtlas.zip")
    extract_path = os.path.join(raw_dir, "FracAtlas")
    
    # URL for FracAtlas on Figshare (Version 7)
    url = "https://ndownloader.figshare.com/files/65518038"
    
    # 2. Check if dataset is already extracted
    if os.path.exists(extract_path):
        print(f"\n[INFO] Dataset is already extracted in: {extract_path}")
        print("You are ready to start training!")
        return
        
    # 3. Check if zip already exists
    if not os.path.exists(zip_path):
        print("\nStarting download from Figshare (approx. 322 MB)...")
        print("Note: This might take a few minutes depending on your internet connection.")
        try:
            urllib.request.urlretrieve(url, zip_path, progress_callback)
            print("\n\n[SUCCESS] Download completed successfully!")
        except Exception as e:
            print(f"\n\n[ERROR] Download failed: {e}")
            print("Please check your internet connection and try running the script again.")
            return
    else:
        print(f"\n[INFO] Found existing zip file at: {zip_path}")
        
    # 4. Unzip the dataset
    print(f"\nExtracting dataset to {extract_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files to show progress
            files = zip_ref.namelist()
            total_files = len(files)
            for i, file in enumerate(files):
                zip_ref.extract(file, extract_path)
                if i % 100 == 0 or i == total_files - 1:
                    sys.stdout.write(f"\rExtracting: {int((i + 1) * 100 / total_files)}% ({i + 1}/{total_files} files)")
                    sys.stdout.flush()
        print("\n\n[SUCCESS] Extraction completed successfully!")
        
        # Optional: Clean up zip file to save disk space
        print("Cleaning up temporary zip file...")
        os.remove(zip_path)
        print("Cleaned up successfully.")
        
    except Exception as e:
        print(f"\n[ERROR] Extraction failed: {e}")
        return

    print("\n=================================================================")
    print("Next Steps:")
    print(f"1. Your dataset is now located at: {extract_path}")
    print("2. It contains the raw X-ray images and standard annotations (COCO, YOLO, VOC).")
    print("3. Would you like me to generate a model training script using this data?")
    print("=================================================================")

if __name__ == "__main__":
    main()
