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
    assert "answer" in output
    assert "FastAPI" in output["answer"]

def test_items_question():
    result = subprocess.run(
        ["uv", "run", "agent.py", "How many items are in the database?"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert "answer" in output
    assert "120" in output["answer"]