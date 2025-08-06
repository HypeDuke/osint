# crawler/regex_processor.py
import os
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from elasticsearch import Elasticsearch
from datetime import datetime

PATTERN_DIR = "./patterns"
INPUT_DIR = "./input_data"
ES_HOST = os.getenv("ES_HOST", "elasticsearch")
ES_PORT = int(os.getenv("ES_PORT", 9200))

es = Elasticsearch([{"host": ES_HOST, "port": ES_PORT}])
INDEX_NAME = "leaked_data"

def load_patterns():
    patterns = []
    for file in os.listdir(PATTERN_DIR):
        if file.endswith(".json"):
            with open(os.path.join(PATTERN_DIR, file), "r", encoding="utf-8") as f:
                pattern_data = json.load(f)
                for item in pattern_data.get("patterns", []):
                    compiled = re.compile(item["pattern"], re.IGNORECASE)
                    patterns.append({"id": item["id"], "regex": compiled})
    return patterns

def process_file(file_path, compiled_patterns):
    results = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                for pattern in compiled_patterns:
                    if pattern["regex"].search(line):
                        results.append({
                            "file": os.path.basename(file_path),
                            "line": i + 1,
                            "content": line.strip(),
                            "pattern_id": pattern["id"],
                            "timestamp": datetime.utcnow().isoformat()
                        })
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
    return results

def save_to_elasticsearch(matches):
    for match in matches:
        es.index(index=INDEX_NAME, body=match)

def main():
    compiled_patterns = load_patterns()
    files = [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.endswith(".txt")
    ]

    all_matches = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {
            executor.submit(process_file, file_path, compiled_patterns): file_path
            for file_path in files
        }

        for future in as_completed(future_to_file):
            matches = future.result()
            if matches:
                save_to_elasticsearch(matches)

if __name__ == "__main__":
    main()
