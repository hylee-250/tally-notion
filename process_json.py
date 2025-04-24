#!/usr/bin/env python3
import sys
import os
from notion_client import process_json_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_json.py <json_file_path>")
        print("Example: python process_json.py response/sub1.json")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    
    if not os.path.isfile(json_file_path):
        print(f"Error: File '{json_file_path}' not found.")
        sys.exit(1)
    
    print(f"Processing JSON file: {json_file_path}")
    results = process_json_file(json_file_path)
    
    print(f"\nProcessed {len(results)} entries:")
    for result in results:
        status = "Success" if result["success"] else "Failed"
        print(f"{result['name']}: {status}")

if __name__ == "__main__":
    main() 