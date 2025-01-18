import os
import sys
import pytest
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from app.main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_count_total" in response.text

def test_metrics_json_endpoint():
    response = client.get("/metrics_json")
    assert response.status_code == 200
    assert "request_count_total" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    health_data = response.json()
    assert "status" in health_data
    assert "request_count" in health_data
    assert "error_count" in health_data
    assert "error_rate" in health_data
    assert "average_latency_seconds" in health_data
    assert "cpu_usage_percent" in health_data
    assert "memory_usage_percent" in health_data

def test_read_yahoo_finance_data():
    response = client.get("/yahoofinance?symbol=VTSMX&price=144.16")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["Symbol"] == "VTSMX"
    assert data[0]["Price (Intraday)"] == "144.16"

# Add more tests for other endpoints and filters
def test_invalid_yahoo_finance_data():
    response = client.get("/yahoofinance?symbol=INVALID")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_metrics_endpoint_request_count():
    initial_metrics = client.get("/metrics").text
    initial_request_count = extract_metric_value(initial_metrics, "request_count_total")

    client.get("/metrics")
    new_metrics = client.get("/metrics").text
    new_request_count = extract_metric_value(new_metrics, "request_count_total")

    assert new_request_count > initial_request_count

def extract_metric_value(metrics_text, metric_name):
    for line in metrics_text.splitlines():
        if line.startswith(metric_name):
            return int(line.split(" ")[-1])
    return 0

# Additional aggressive test cases can be added as needed
