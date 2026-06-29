"""API integration tests for BPM Frontend application.

These tests validate endpoint contracts and are designed to run
against a live instance. Set BASE_URL environment variable to
point at the target environment (defaults to localhost for CI).
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('BASE_URL', 'http://localhost:80')


@pytest.fixture(scope='session')
def api_base():
    return BASE_URL


class TestHealthCheckContract:
    """Validate the health check contract required by the ALB target group."""

    def test_health_endpoint_reachable(self, api_base):
        """ALB requires /health to return 200 for traffic routing."""
        try:
            response = requests.get(f'{api_base}/health', timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip('Live environment not available - skipping integration test')

    def test_health_response_schema(self, api_base):
        """Health response must conform to expected schema."""
        try:
            response = requests.get(f'{api_base}/health', timeout=5)
            data = response.json()
            assert 'status' in data
            assert 'service' in data
            assert 'version' in data
        except requests.exceptions.ConnectionError:
            pytest.skip('Live environment not available - skipping integration test')


class TestAPIStatusContract:
    """Validate the /api/status endpoint contract."""

    def test_status_endpoint_reachable(self, api_base):
        """Status endpoint must be reachable."""
        try:
            response = requests.get(f'{api_base}/api/status', timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip('Live environment not available - skipping integration test')

    def test_status_content_type(self, api_base):
        """Status endpoint must return application/json."""
        try:
            response = requests.get(f'{api_base}/api/status', timeout=5)
            assert 'application/json' in response.headers.get('Content-Type', '')
        except requests.exceptions.ConnectionError:
            pytest.skip('Live environment not available - skipping integration test')
