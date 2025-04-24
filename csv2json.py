import csv
import json

csv_file = 'response/sub1.csv'
json_file = 'response/sub1.json'

data = []

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ JSON 파일로 변환 완료:", json_file)