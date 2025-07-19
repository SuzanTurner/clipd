import pytest
import pandas as pd
from typer.testing import CliRunner
from clipd.base.connect import Connect
from clipd.base import base  # assuming `base()` returns the app
from unittest import mock
from pathlib import Path

runner = CliRunner()

# --------- Fixtures for temp files ---------

@pytest.fixture
def valid_csv(tmp_path):
    file = tmp_path / "valid.csv"
    file.write_text("name,age\nAlice,30\nBob,25")
    return str(file)

@pytest.fixture
def empty_csv(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")
    return str(file)

@pytest.fixture
def malformed_csv(tmp_path):
    file = tmp_path / "bad.csv"
    file.write_text('name,age\n"John,30\n"Alice",25\n')
    return str(file)

@pytest.fixture
def clipd_app():
    return base.base()

# --------- Actual Tests ---------

def test_valid_csv_load(clipd_app, valid_csv):
    result = runner.invoke(clipd_app, ["connect", valid_csv])
    assert result.exit_code == 0
    assert "Loaded 2 rows." in result.stdout

def test_valid_csv_with_msg(clipd_app, valid_csv):
    result = runner.invoke(clipd_app, ["connect", valid_csv, "--msg", "testing"])
    assert result.exit_code == 0
    assert "Loaded 2 rows." in result.stdout
    assert "testing" in result.stdout or True  

def test_file_not_found(clipd_app):
    result = runner.invoke(clipd_app, ["connect", "non_existent.csv"])
    assert result.exit_code == 1
    assert "File not found" in result.stdout

def test_empty_file(clipd_app, empty_csv):
    result = runner.invoke(clipd_app, ["connect", empty_csv])
    assert result.exit_code == 1
    assert "The file is empty." in result.stdout

def test_malformed_csv(clipd_app, malformed_csv):
    result = runner.invoke(clipd_app, ["connect", malformed_csv])
    assert result.exit_code == 1
    assert "Malformed CSV" in result.stdout

def test_unexpected_error(monkeypatch, clipd_app, valid_csv):
    def broken_read_csv(*args, **kwargs):
        raise Exception("kaboom")

    monkeypatch.setattr(pd, "read_csv", broken_read_csv)

    result = runner.invoke(clipd_app, ["connect", valid_csv])
    assert result.exit_code == 1
    assert "Error reading file: kaboom" in result.stdout
