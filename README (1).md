
# OptiBot – AI-Powered Help Center Assistant

This project scrapes OptiSigns Help Center articles, converts them into Markdown, and uploads them to an OpenAI Vector Store for use in a custom GPT Assistant. It runs daily using a cron job on a DigitalOcean Droplet.

---

## ✅ Features

- Automatically fetches articles from Zendesk Help Center API.
- Cleans and converts content into structured Markdown.
- Uploads new/updated articles to OpenAI Vector Store.
- Tracks content hashes to prevent duplicate uploads.
- Scheduled to run daily via cron on a DigitalOcean Droplet.

---

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- Docker & Docker Hub account
- OpenAI API key (for Vector Store)
- DigitalOcean Droplet (Ubuntu)
- Git

### Environment Setup

1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd optibot
   ```

2. Set up Python environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in `main.py`:
   ```python
   client = OpenAI(api_key="your-api-key")
   ```

4. Run locally:
   ```bash
   python main.py
   ```

---

## 🐳 Docker & Deployment

### Build Docker Image
```bash
docker build -t optibot .
```

### Push to Docker Hub
```bash
docker tag optibot <your-dockerhub-username>/optibot
docker push <your-dockerhub-username>/optibot
```

---

## ☁️ Deploy with Cron on DigitalOcean

1. Create a new Droplet via [DigitalOcean](https://cloud.digitalocean.com).
2. SSH into your Droplet:
   ```bash
   ssh root@<your-droplet-ip>
   ```
3. Clone your repo & install Docker if needed.
4. Pull the latest image:
   ```bash
   docker pull <your-dockerhub-username>/optibot
   ```

5. Create `run.sh` script:
   ```bash
   #!/bin/bash
   docker run --rm <your-dockerhub-username>/optibot
   ```

6. Make it executable:
   ```bash
   chmod +x run.sh
   ```

7. Add cron job:
   ```bash
   crontab -e
   ```
   Add this line to run daily at 7AM UTC:
   ```cron
   0 7 * * * /bin/bash /root/optibot/run.sh >> /root/optibot/cron.log 2>&1
   ```

---

## 📜 Log Access

You can check the log output with:
```bash
cat /root/optibot/cron.log
```

### Log Entry Example
```
Upload done: 100 total, ✅ 98 completed.
Log counts:
Added: 2
Updated: 3
Skipped: 95
Last run: 2025-07-24T07:00:01
```

---

## 🧠 Assistant Playground Screenshot

Below is a screenshot of the GPT assistant properly answering support queries with citation from articles:

![GPT Assistant Screenshot](./screenshot.jpg)

---

## ✅ Deliverables

- [x] Dockerized scraper and uploader
- [x] Auto upload to Vector Store
- [x] Daily cronjob on DigitalOcean
- [x] Assistant playground screenshot
- [x] README with setup, run, logs

---

## License

MIT License – Free to use and modify for internal testing and educational purposes.
