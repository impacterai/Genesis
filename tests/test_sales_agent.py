import json
import importlib.util
from pathlib import Path
from unittest import mock

MODULE_DIR = Path(__file__).resolve().parent.parent / "ImpacterAI Genesis Machine"
spec = importlib.util.spec_from_file_location("sales_agent", MODULE_DIR / "sales_agent.py")
sales_agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sales_agent)
SalesAgenticSystem = sales_agent.SalesAgenticSystem
load_sales_tasks = sales_agent.load_sales_tasks


def test_load_sales_tasks(tmp_path):
    data = [
        {"description": "Task one"},
        {"description": "Task two"},
    ]
    file = tmp_path / "tasks.json"
    file.write_text(json.dumps(data))
    tasks = load_sales_tasks(str(file))
    assert tasks == ["Task one", "Task two"]


def test_sales_agent_forward(monkeypatch, tmp_path):
    def fake_chat(msg, model=None, msg_history=None, logging=None):
        return []

    monkeypatch.setattr(sales_agent, "chat_with_agent", fake_chat)

    agent = SalesAgenticSystem(
        sales_strategy="Test strategy",
        git_tempdir=str(tmp_path),
        base_commit="HEAD",
        chat_history_file=str(tmp_path / "chat.md"),
    )
    # Should run without error
    agent.forward()
