from typer.testing import CliRunner
from clipd.base import base 
import pytest

runner = CliRunner()

def test_init(monkeypatch):
    logs = {}

    def mock_log_command(command, detail, status, msg):
        logs["command"] = command
        logs["detail"] = detail
        logs["status"] = status
        logs["msg"] = msg

    monkeypatch.setattr("clipd.base.init.log_command", mock_log_command)

    app = base.base()  

    result = runner.invoke(app, ["init", "--msg", "pytest was here"])

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.exit_code == 0
    assert "Clipd Reinitialised!\nConnected to session C:\\Users\\HP\\.clipd_session.json\n" in result.stdout
    assert logs == {
        "command": "init --msg",
        "detail": "Clipd Initialised",
        "status": "Completed",
        "msg": "pytest was here"
    }
