import argparse
from tabulate import tabulate
import json


def parse_args():
    parser = argparse.ArgumentParser(
        prog='ResponseTimeAnalyzer',
        description='Analyzes response times from JSON log file',
        epilog='Text at the bottom of help'
    )
    parser.add_argument('--file', help='JSON file path') 
    parser.add_argument('--report', help='Output report file path (optional)')
    return parser.parse_args()

def read_and_parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content:
            return []
        lines = content.split('\n')
        return [json.loads(line) for line in lines if line.strip()]

def calculate_stats(data):
    if not data:
        return []
    
    set_url = set(item['url'] for item in data)
    results = [["handler", "total", "avg_response_time"]]
    
    for j, handler in enumerate(set_url):
        lst_time = [item['response_time'] for item in data if item.get('url') == handler]
        sum_time = sum(lst_time)
        avg_time = round(sum_time / len(lst_time), 3)
        results.append([j, handler, sum_time, avg_time])

    return results

def generate_report(stats, output_file=None):
    report = tabulate(stats, headers="firstrow", tablefmt="grid")
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
    
    return report

def main():
    args = parse_args()
    data = read_and_parse_json_file(args.file)
    stats = calculate_stats(data)
    report = generate_report(stats, args.report)
    print(report)

if __name__ == "__main__":
    main()