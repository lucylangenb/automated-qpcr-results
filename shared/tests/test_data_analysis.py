import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) #look for custom dependencies in shared folder

import pytest
import pandas as pd
from io import StringIO
from shared.data_analysis import DataImporter, DataAnalyzer

# tests/test_data_analysis.py


class DummyTk:
    def withdraw(self): pass

@pytest.fixture
def importer(monkeypatch):
    # Patch tkinter and tomli
    monkeypatch.setattr("tkinter.Tk", lambda: DummyTk())
    monkeypatch.setattr("tomli.load", lambda f: {
        "testassay": {
            "assay": {"FAM": "Target1", "HEX": "Internal Control"},
            "ic": "HEX"
        }
    })
    return DataImporter(assay="testassay", machine_type="Mic", division="hiv")

def test_isblank(importer):
    assert importer.isblank(['', '', '']) is True
    assert importer.isblank(['', 'a', '']) is False

def test_csv_to_df(importer):
    csv_content = StringIO("Header1,Header2\nResults,Data\nWell,Ct\n1,2\n3,4\n")
    # Simulate file-like object
    df = importer.csv_to_df(csv_content, ',', 'Results')
    assert list(df.columns) == ['Well', 'Ct']
    assert df.iloc[0, 0] == '1'

def test_summarize(importer):
    df1 = pd.DataFrame({'Well': [1], 'Sample Name': ['A'], 'FAM CT': [20], 'FAM Quantity': [100]})
    df2 = pd.DataFrame({'Well': [1], 'Sample Name': ['A'], 'HEX CT': [22], 'HEX Quantity': [200]})
    importer.machine_type = "Mic"
    importer.division = "hiv"
    result = importer.summarize({'FAM': df1, 'HEX': df2})
    assert 'FAM CT' in result.columns
    assert 'HEX CT' in result.columns

def test_extract_header(importer):
    rows = [
        ['Experiment', 'Info'],
        ['Header', 'Value'],
        ['Stop', 'Here'],
        ['Data', 'Row']
    ]
    reader = iter(rows)
    header = importer.extract_header(reader, flag='Experiment', stop='Stop')
    assert ['Experiment', 'Info'] in header

def test_extract_results(importer):
    df = pd.DataFrame([
        ['Well', 'Sample Name', 'FAM CT'],
        ['1', 'A', '20'],
        ['2', 'B', '22']
    ])
    df.columns = [0, 1, 2]
    result = importer.extract_results(df)
    assert 'Well' in result.columns

def test_vhf_result():
    class DummyData:
        results = pd.DataFrame()
        machine_type = "QuantStudio 3"
        reporter_dict = {"HEX": "Internal Control", "FAM": "Target1"}
        reporter_list = ["HEX", "FAM"]
        ic = "HEX"
        max_dRn_dict = {"FAM": 100}
        cq_cutoff = 35
    data = DummyData()
    analyzer = DataAnalyzer(data)
    row = pd.Series({"HEX CT": 25, "FAM CT": 20, "FAM dRn": 10})
    result = analyzer.vhf_result(row)
    assert result in ["Target1 Positive", "Negative", "Invalid Result"]

def test_hiv_result():
    class DummyData:
        results = pd.DataFrame()
        machine_type = "Mic"
        reporter_dict = {"HEX": "Internal Control", "FAM": "Target1"}
        reporter_list = ["HEX", "FAM"]
        ic = "HEX"
        max_dRn_dict = {"FAM": 100}
        cq_cutoff = 35
    data = DummyData()
    analyzer = DataAnalyzer(data)
    row = {"Target1 DRM Percentage": 0.12, "HEX Quantity": 100}
    call = analyzer.hiv_result(row, "Target1 DRM Percentage")
    assert call in ["Negative", "Positive", "Indeterminate"]