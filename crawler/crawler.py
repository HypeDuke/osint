import re
import os
import json
import datetime
import requests

ELASTICSEARCH_URL = "http://elasticsearch:9200/leaks/_doc"

# Danh sách từ khóa hoặc domain cần lọc
TARGET_PATTERNS = [r"[\w\.-]+@bank\.vn", r"[\w\.-]+@company\.com"]

# File dữ liệu mẫu
DATA_FILE = "leak_sample.txt"

# Hàm trích xuất email từ dòng văn bản
def extract_emails(line):
    matches = []
    for pattern in TARGET_PATTERNS:
        found = re.findall(pattern, line)
        matches.extend(found)
    return matches

# Gửi 1 leak vào Elasticsearch
def send_to_elasticsearch(data):
    response = requests.post(ELASTICSEARCH_URL, json=data)
    if response.status_code not in (200, 201):
        print("[ERROR] Failed to push to Elasticsearch:", response.text)

# Đọc từng dòng file và xử lý
def process_file():
    if not os.path.exists(DATA_FILE):
        print(f"File not found: {DATA_FILE}")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            emails = extract_emails(line)
            if emails:
                for email in emails:
                    domain = email.split("@")[-1]
                    doc = {
                        "source": "local_file",
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "raw_data": line.strip(),
                        "emails": [email],
                        "domain": domain,
                        "leak_type": "email"
                    }
                    send_to_elasticsearch(doc)
                    print("[+] Leak sent:", email)

if __name__ == "__main__":
    process_file()
