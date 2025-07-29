import os
import json
import hashlib
from datetime import datetime
from scrape import scrape_and_save
from bot import create_vector_store, upload_files_to_vector_store, create_assistant_with_vector_store
from openai import OpenAI

# Constants
MARKDOWN_DIR = "markdown_articles"
METADATA_PATH = "metadata_store.json"

# API Key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)
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
        print("Creating vector store and uploading files...")
        vector_store = create_vector_store()
        file_streams = [open(os.path.join(MARKDOWN_DIR, f), "rb") for f in files_to_upload]
        upload_files_to_vector_store(vector_store.id, file_streams)
        # Create assistant using the uploaded vector store
        assistant = create_assistant_with_vector_store(vector_store.id)
        print(f"Assistant created with ID: {assistant.id}")

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
