import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock
from src.req import fetch_pdf_from_url
from pathlib import Path

def test_fetch_pdf_from_url_local_file(tmp_path):
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes(b"Sample PDF content")
    pdf_data = fetch_pdf_from_url(str(file_path))
    assert isinstance(pdf_data, BytesIO)
    assert pdf_data.read() == b"Sample PDF content"

@patch("src.req.requests.get")
def test_fetch_pdf_from_url_link(mock_get):
    # Mocking a PDF response from the URL
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Sample PDF from URL"
    mock_get.return_value = mock_response

    pdf_data = fetch_pdf_from_url("http://example.com/test.pdf")
    assert isinstance(pdf_data, BytesIO)
    assert pdf_data.read() == b"Sample PDF from URL"
    mock_get.assert_called_once_with("http://example.com/test.pdf")
