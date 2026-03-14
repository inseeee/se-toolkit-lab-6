import subprocess
import json

def test_framework_question():
    result = subprocess.run(
        ["uv", "run", "agent.py", "What Python web framework does this project use?"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert "tool_calls" in output
    assert any(t["tool"] == "read_file" for t in output["tool_calls"])

def test_item_count_question():
    result = subprocess.run(
        ["uv", "run", "agent.py", "How many items are in the database?"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert "tool_calls" in output
    assert any(t["tool"] == "query_api" for t in output["tool_calls"])