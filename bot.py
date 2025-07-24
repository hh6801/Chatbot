import os
import warnings
from openai import OpenAI

# Bỏ qua cảnh báo Deprecation
warnings.filterwarnings("ignore", category=DeprecationWarning)


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def create_vector_store(name="KnowledgeBase"):
    vector_store = client.vector_stores.create(name=name)
    print(f"Vector store created: {vector_store.id}")
    return vector_store

def load_markdown_files(folder_path):
    file_paths = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".md") and os.path.getsize(os.path.join(folder_path, f)) > 0
    ]
    streams = [open(path, "rb") for path in file_paths]
    print(f"{len(streams)} markdown files loaded for upload.")
    return streams, file_paths

def upload_files_to_vector_store(vector_store_id, file_streams):
    print("Uploading files...")
    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id,
        files=file_streams
    )
    print("Upload complete:")
    print(f" - Completed: {file_batch.file_counts.completed}")
    print(f" - Failed: {file_batch.file_counts.failed}")
    print(f" - Total: {file_batch.file_counts.total}")
    print(f" - Status: {file_batch.status}")
    return file_batch

def list_files_in_vector_store(vector_store_id):
    print("Listing files in vector store...")
    file_list = client.vector_stores.files.list(vector_store_id=vector_store_id)
    if not file_list.data:
        print("No files found in vector store.")
        return
    print(f"Vector store contains {len(file_list.data)} files:")
    for f in file_list.data:
        file_info = client.files.retrieve(f.id)
        print(f"- {file_info.filename} (ID: {file_info.id})")

def create_assistant_with_vector_store(vector_store_id):
    assistant = client.beta.assistants.create(
        name="OptiSigns Markdown Assistant",
        instructions = """
        You are OptiBot, the customer-support bot for OptiSigns.com.
        Tone: helpful, factual, concise.
        Only answer using the uploaded docs.
        Max 5 bullet points; else link to the doc.
        Cite up to 3 "Article URL:" lines per reply.
        """,
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
    )
    print("Assistant created.")
    print(f"- Assistant ID: {assistant.id}")
    return assistant

def main():
    # Step 1: Create vector store
    vector_store = create_vector_store()

    # Step 2: Load markdown files
    file_streams, file_paths = load_markdown_files("markdown_articles")
    if not file_streams:
        print("No valid .md files to upload. Exiting.")
        return

    # Step 3: Upload to vector store
    upload_files_to_vector_store(vector_store.id, file_streams)

    # Step 4: Verify uploaded files
    list_files_in_vector_store(vector_store.id)

    # Step 5: Create assistant
    assistant = create_assistant_with_vector_store(vector_store.id)

    # Step 6: Print final info
    print("\nAssistant and vector store are ready to use.")
    print(f"Assistant ID: {assistant.id}")
    print(f"Vector Store ID: {vector_store.id}")

if __name__ == "__main__":
    main()
