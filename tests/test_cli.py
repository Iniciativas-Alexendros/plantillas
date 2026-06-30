from typer.testing import CliRunner

from plantillas.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "2.0.0-dev" in result.output


def test_config():
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "Versión del catálogo" in result.output


def test_validate_unknown_module():
    result = runner.invoke(app, ["validate", "no-existe"])
    assert result.exit_code == 1
    assert "Módulo desconocido" in result.output


def test_validate_agent_config():
    result = runner.invoke(app, ["validate", "agent-config"])
    assert result.exit_code == 0
    assert "agent-config: OK" in result.output


def test_validate_all():
    result = runner.invoke(app, ["validate"])
    assert result.exit_code == 0
    assert "agent-config" in result.output
