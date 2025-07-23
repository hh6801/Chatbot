import os
import warnings
from openai import OpenAI

# Bỏ qua cảnh báo Deprecation
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI(api_key= "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")  # Thay YOUR_API_KEY bằng key thật
# Liệt kê và xoá toàn bộ file đã upload
files = client.files.list()

for f in files.data:
    print(f"🗑️ Xoá file: {f.id} - {f.filename}")
    client.files.delete(f.id)