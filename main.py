import os
import json
import hashlib
from datetime import datetime
from openai import OpenAI
from scrape import scrape_and_save

# Cấu hình
MARKDOWN_DIR = "markdown_articles"
METADATA_PATH = "metadata_store.json"
VECTOR_STORE_ID = "vs_687fb88fef8081919623096963c58dec"
client = OpenAI(api_key= "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")
added, updated, skipped = 0, 0, 0

def ensure_directories():
    os.makedirs(MARKDOWN_DIR, exist_ok=True)

def calculate_file_hash(path):
    with open(path, "r", encoding="utf-8") as f:
        return hashlib.md5(f.read().encode("utf-8")).hexdigest()

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def get_markdown_files():
    return [f for f in os.listdir(MARKDOWN_DIR) if f.endswith(".md")]

def upload_to_vector_store(files):
    file_streams = [open(os.path.join(MARKDOWN_DIR, f), "rb") for f in files]
    response = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=VECTOR_STORE_ID,
        files=file_streams
    )
    print(f"\nUpload done: {response.file_counts.total} total,  {response.file_counts.completed} completed.")

def main():
    global added, updated, skipped
    ensure_directories()
    scrape_and_save()

    metadata = load_metadata()
    markdown_files = get_markdown_files()
    files_to_upload = []

    for filename in markdown_files:
        path = os.path.join(MARKDOWN_DIR, filename)
        current_hash = calculate_file_hash(path)

        if filename not in metadata:
            metadata[filename] = {"hash": current_hash}
            files_to_upload.append(filename)
            added += 1
        elif metadata[filename]["hash"] != current_hash:
            metadata[filename]["hash"] = current_hash
            files_to_upload.append(filename)
            updated += 1
        else:
            skipped += 1

    if files_to_upload:
        upload_to_vector_store(files_to_upload)
    else:
        print("No new or updated files to upload.")

    save_metadata(metadata)

    # Logging
    print("\nLog counts:")
    print(f"Added: {added}")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print(f"Last run: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
