# 🤖 OptiBot – Zendesk Article Scraper & OpenAI Vector Store Uploader

OptiBot là một bot hỗ trợ khách hàng của [OptiSigns.com](https://www.optisigns.com), giúp tự động:
- Thu thập dữ liệu bài viết từ Zendesk Help Center (support.optisigns.com)
- Chuyển thành markdown
- Tải lên OpenAI Vector Store
- Dùng để hỗ trợ cho Assistant API với khả năng tìm kiếm theo ngữ nghĩa (semantic retrieval)

---

## 🔧 Setup

### 1. Clone Repo & Cài đặt

```bash
git clone https://github.com/your-username/optibot.git
cd optibot
```

### 2. Cài thư viện Python

Tạo môi trường ảo (tùy chọn):

```bash
python -m venv venv
source venv/bin/activate
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

> `requirements.txt` gồm:
```
requests
beautifulsoup4
openai
```

---

## ▶️ How to Run Locally

### 1. Cấu trúc chính

| File                | Vai trò |
|---------------------|--------|
| `scrape.py`         | Cào dữ liệu từ Zendesk, chuyển thành Markdown |
| `main.py`           | Gọi `scrape.py`, kiểm tra thay đổi, upload lên OpenAI Vector Store |
| `metadata_store.json` | Lưu hash để tránh upload trùng lặp |
| `markdown_articles/` | Chứa các file `.md` đã tạo |

### 2. Chạy thủ công:

```bash
python main.py
```

Kết quả sẽ được ghi log như:

```
Total 100 articles saved in `markdown_articles`
Upload done: 100 total, ✅ 98 completed.
Log counts:
Added: 2
Updated: 3
Skipped: 95
```

---

## 🚀 Docker & Deploy

### 1. Build và Push Image

```bash
docker build -t hh68201/optibot .
docker tag hh68201/optibot hh68201/optibot:latest
docker push hh68201/optibot
```

### 2. Tạo cron job với Droplet (DigitalOcean)

**File `/root/optibot/run.sh`:**
```bash
#!/bin/bash
cd /root/optibot
docker pull hh68201/optibot
docker run --rm hh68201/optibot >> /root/optibot/cron.log 2>&1
```

**Crontab (chạy lúc 7h sáng UTC hằng ngày):**
```bash
crontab -e
```
```cron
0 7 * * * /bin/bash /root/optibot/run.sh >> /root/optibot/cron.log 2>&1
```

---

## 📝 Daily Job Logs

Logs được lưu tại:

```bash
/root/optibot/cron.log
```

Kiểm tra log chạy:

```bash
cat /root/optibot/cron.log
```

Hoặc thời gian gần nhất:

```bash
grep CRON /var/log/syslog | tail
```

---

## 📷 Screenshot: Assistant Playground

| ✅ Truy vấn OptiBot trong Playground (Assistant API) |
|-----------------------------------------------------|
| ![Playground Screenshot](./screenshots/playground_answer.png) |

> Assistant trả về nội dung từ bài viết đã tải lên vector store thành công.

---

## 🧼 Notes

- Dùng `article["id"]` làm tên file để tránh trùng lặp slug như `how-to-add-video.md`, `how-to-add-video-1.md`.
- Dữ liệu `.md` được hash kiểm tra để tránh re-upload nếu không đổi nội dung.
- Đã tối ưu để không lưu trùng và chỉ cập nhật nếu bài viết có thay đổi.

---

## ✅ Deliverables Checklist

- [x] ✅ Vector store setup & file upload
- [x] ✅ Scraper using Zendesk API
- [x] ✅ Markdown transformation & metadata
- [x] ✅ Dockerized pipeline
- [x] ✅ Scheduled daily job via DigitalOcean Droplet + Cron
- [x] ✅ Log file + Playground screenshot
