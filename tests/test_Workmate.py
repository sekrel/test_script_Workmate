import pytest
import sys
from src.workmate.main import parse_args, read_and_parse_json_file, calculate_stats, generate_report, main


@pytest.fixture
def create_file(tmp_path):
    test_file = tmp_path / "test_file.log"
    content= '''{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.02, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.032, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.064, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.1, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.076, "http_user_agent": "..."}
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.076, "http_user_agent": "..."}
    '''
    dict_content = [{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.02, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/context/...", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.032, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.06, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.064, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.1, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.076, "http_user_agent": "..."},
    {"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/homeworks/...", "request_method": "GET", "response_time": 0.076, "http_user_agent": "..."}]
    test_file.write_text(content)
    assert test_file.exists()
    return test_file, dict_content
    

@pytest.fixture
def create_simplified_file(tmp_path):
    simplified_test_file = tmp_path / "simplified_test_file.log"
    content='''{"url": "/api/users", "response_time": 0.1}
    {"url": "/api/products", "response_time": 0.2}
    {"url": "/api/users", "response_time": 0.15}
    {"url": "/api/products", "response_time": 0.25}
    {"url": "/api/orders", "response_time": 0.3}
    '''
    simplified_test_file.write_text(content)
    assert simplified_test_file.exists()
    return simplified_test_file

@pytest.fixture
def empty_json_file(tmp_path):
    test_file = tmp_path / "test_file.log"
    test_file.write_text("")
    return test_file

def test_read_and_parse_normal_file(create_file):
    file_log, dict_log  = create_file
    data = read_and_parse_json_file(file_log)
    assert data == dict_log
    
def test_read_and_parse_empty_file(empty_json_file):
    data = read_and_parse_json_file(empty_json_file)
    assert data == []

def test_calculate_stats():
    test_data = [
        {'url': '/api/users', 'response_time': 0.1},
        {'url': '/api/users', 'response_time': 0.2},
        {'url': '/api/products', 'response_time': 0.3}
    ]
    stats = calculate_stats(test_data)
    assert len(stats) == 3  # header + 2 handlers
    assert stats[0] == ["handler", "total", "avg_response_time"]

    users_stats = next(row for row in stats if '/api/users' in row)
    products_stats = next(row for row in stats if '/api/products' in row)
    assert users_stats[2] == pytest.approx(0.3)  # total time
    assert users_stats[3] == pytest.approx(0.15)  # avg time
    assert products_stats[2] == pytest.approx(0.3)  # total time
    assert products_stats[3] == pytest.approx(0.3)  # avg time

def test_calculate_stats_empty_data():
    stats = calculate_stats([])
    assert stats == []

def test_generate_report(tmp_path):
    stats = [
        ["handler", "total", "avg_response_time"],
        [0, "/api/users", 0.3, 0.15],
        [1, "/api/products", 0.3, 0.3]
    ]
    report = generate_report(stats)
    assert "handler" in report
    assert "/api/users" in report
    assert "0.15" in report
    
    output_file = tmp_path / "report.txt"
    report = generate_report(stats, output_file)
    assert output_file.exists()
    assert "handler" in output_file.read_text()

def test_integration(create_simplified_file, tmp_path, capsys):
    content = create_simplified_file
    test_args = ['--file', str(content), '--report', str(tmp_path / "output.txt")]
    original_argv = sys.argv

    try:
        sys.argv = ['test'] + test_args
        main()

        captured = capsys.readouterr()
        assert "handler" in captured.out
        assert "/api/users" in captured.out

        report_file = tmp_path / "output.txt"
        assert report_file.exists()
        report_content = report_file.read_text()
        assert "handler" in report_content
    finally:
        sys.argv = original_argv
