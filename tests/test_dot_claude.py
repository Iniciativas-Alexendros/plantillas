"""
Tests unitarios para el validador de dot-claude.

Ejecutar:
    pytest tests/test_dot_claude.py -v
"""

import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import Nivel

PLANTILLAS = Path(__file__).resolve().parents[1]

# Importar el validador de dot-claude (directorio con guión, no importable como paquete)
_dot_claude_path = PLANTILLAS / "dot-claude" / "validar_dot_claude.py"
_spec = importlib.util.spec_from_file_location("validar_dot_claude", _dot_claude_path)
_validar_dot_claude = importlib.util.module_from_spec(_spec)
sys.modules["validar_dot_claude"] = _validar_dot_claude
_spec.loader.exec_module(_validar_dot_claude)
DotClaudeValidator = _validar_dot_claude.DotClaudeValidator


class TestCheckSettingsJson:
    def _valid_settings(self):
        return {
            "permissions": {"allow": ["Bash"], "deny": []},
            "hooks": {
                "SessionStart": [
                    {
                        "matcher": ".*",
                        "hooks": [{"type": "command", "command": "echo ok"}],
                    }
                ]
            },
        }

    def test_settings_valido_devuelve_ok(self, tmp_path):
        (tmp_path / "settings.json").write_text(
            json.dumps(self._valid_settings()), encoding="utf-8"
        )
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.OK for r in resultados)
        assert not any(r.nivel == Nivel.ERROR for r in resultados)

    def test_json_invalido(self, tmp_path):
        (tmp_path / "settings.json").write_text("{invalid", encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "JSON inválido" in r.mensaje for r in resultados)

    def test_no_es_dict(self, tmp_path):
        (tmp_path / "settings.json").write_text("[]", encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "objeto JSON" in r.mensaje for r in resultados)

    def test_falta_permissions(self, tmp_path):
        data = self._valid_settings()
        del data["permissions"]
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "permissions" in r.mensaje for r in resultados)

    def test_permissions_no_es_dict(self, tmp_path):
        data = self._valid_settings()
        data["permissions"] = []
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "permissions' debe ser un objeto" in r.mensaje for r in resultados)

    def test_falta_allow_deny(self, tmp_path):
        data = self._valid_settings()
        data["permissions"] = {}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "allow" in r.mensaje for r in resultados)
        assert any(r.nivel == Nivel.ERROR and "deny" in r.mensaje for r in resultados)

    def test_allow_deny_no_lista(self, tmp_path):
        data = self._valid_settings()
        data["permissions"] = {"allow": "Bash", "deny": "Bash"}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "permissions.allow' debe ser una lista" in r.mensaje for r in resultados)
        assert any(r.nivel == Nivel.ERROR and "permissions.deny' debe ser una lista" in r.mensaje for r in resultados)

    def test_allow_con_elemento_no_string(self, tmp_path):
        data = self._valid_settings()
        data["permissions"] = {"allow": [123], "deny": []}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "no-string" in r.mensaje for r in resultados)

    def test_falta_hooks(self, tmp_path):
        data = self._valid_settings()
        del data["hooks"]
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "hooks" in r.mensaje for r in resultados)

    def test_hooks_no_es_dict(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = []
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "hooks' debe ser un objeto" in r.mensaje for r in resultados)

    def test_evento_no_reconocido_warning(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {"FooEvent": []}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.WARNING and "FooEvent" in r.mensaje for r in resultados)

    def test_hooks_evento_no_lista(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {"SessionStart": {}}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "SessionStart' debe ser una lista" in r.mensaje for r in resultados)

    def test_entrada_hook_no_dict(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {"SessionStart": ["invalid"]}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "debe ser un objeto" in r.mensaje for r in resultados)

    def test_falta_matcher(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {"SessionStart": [{"hooks": []}]}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "matcher" in r.mensaje for r in resultados)

    def test_falta_hooks_lista(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {"SessionStart": [{"matcher": ".*"}]}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "falta 'hooks'" in r.mensaje for r in resultados)

    def test_comando_no_dict(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {"SessionStart": [{"matcher": ".*", "hooks": ["invalid"]}]}
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "hooks[0]' debe ser un objeto" in r.mensaje for r in resultados)

    def test_tipo_no_command(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {
            "SessionStart": [
                {
                    "matcher": ".*",
                    "hooks": [{"type": "shell", "command": "echo ok"}],
                }
            ]
        }
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "type' debe ser 'command'" in r.mensaje for r in resultados)

    def test_command_vacio(self, tmp_path):
        data = self._valid_settings()
        data["hooks"] = {
            "SessionStart": [
                {"matcher": ".*", "hooks": [{"type": "command", "command": ""}]}
            ]
        }
        (tmp_path / "settings.json").write_text(json.dumps(data), encoding="utf-8")
        v = DotClaudeValidator(tmp_path, strict=False)
        resultados = v._check_settings_json()
        assert any(r.nivel == Nivel.ERROR and "command' debe ser string no vacío" in r.mensaje for r in resultados)
