import pytest
import pandas as pd
from main import create_cluster_plot, create_bar_plot, create_heatmap, create_pie_chart
from matplotlib.figure import Figure

@pytest.fixture
def sample_incident_data():
    data = [
        {"date_time": "2024-01-01 12:00", "incident_number": "12345", "location": "Main St", "nature": "Theft", "incident_ori": "OK123"},
        {"date_time": "2024-01-02 14:30", "incident_number": "67890", "location": "Elm St", "nature": "Assault", "incident_ori": "OK456"},
        {"date_time": "2024-01-03 10:00", "incident_number": "54321", "location": "Main St", "nature": "Theft", "incident_ori": "OK123"},
        {"date_time": "2024-01-04 16:45", "incident_number": "98765", "location": "Pine St", "nature": "Burglary", "incident_ori": "OK789"},
        {"date_time": "2024-01-05 09:15", "incident_number": "11111", "location": "Elm St", "nature": "Assault", "incident_ori": "OK456"},
    ]
    return pd.DataFrame(data)

def test_create_cluster_plot(sample_incident_data):
    """Test that create_cluster_plot generates a valid figure."""
    fig = create_cluster_plot(sample_incident_data)
    assert isinstance(fig, Figure), "Cluster plot did not return a matplotlib Figure"

def test_create_bar_plot(sample_incident_data):
    """Test that create_bar_plot generates a valid figure."""
    fig = create_bar_plot(sample_incident_data)
    assert isinstance(fig, Figure), "Bar plot did not return a matplotlib Figure"

def test_create_heatmap(sample_incident_data):
    """Test that create_heatmap generates a valid figure."""
    fig = create_heatmap(sample_incident_data)
    assert isinstance(fig, Figure), "Heatmap did not return a matplotlib Figure"

def test_create_pie_chart(sample_incident_data):
    """Test that create_pie_chart generates a valid figure."""
    fig = create_pie_chart(sample_incident_data)
    assert isinstance(fig, Figure), "Pie chart did not return a matplotlib Figure"
