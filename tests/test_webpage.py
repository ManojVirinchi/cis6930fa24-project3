import pytest
import subprocess
import time
import requests

@pytest.fixture(scope="module")
def start_gradio_server():
    process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    yield process  
    process.terminate()

def test_gradio_page_generated(start_gradio_server):
    """Test that the Gradio webpage is being generated."""
    try:
        response = requests.get("http://127.0.0.1:5003")
        
        assert response.status_code == 200
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Gradio web page not generated. Error: {e}")
