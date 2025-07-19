
from typer.testing import CliRunner
from clipd.base.base import Base
import typer

cli = typer.Typer()
cli.command()(Base.init)
runner = CliRunner()

def test_init(monkeypatch):
    logs = {}

    def mock_log_command(command, detail, status, msg):
        logs["command"] = command
        logs["detail"] = detail
        logs["status"] = status
        logs["msg"] = msg

    monkeypatch.setattr("clipd.base.base.log_command", mock_log_command)

    result = runner.invoke(cli, ["--msg", "pytest was here"])

    assert "Clipd Initialised!" in result.stdout
    assert result.exit_code == 0
    assert logs == {
        "command": "init",
        "detail": "Clipd Initialised",
        "status": "Completed",
        "msg": "pytest was here"
    }

