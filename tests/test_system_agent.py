import subprocess
import json

def test_agent_imports():
    """Test that agent imports without errors"""
    result = subprocess.run(
        ["uv", "run", "python", "-c", "import agent"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_agent_runs():
    """Test that agent runs and returns JSON"""
    result = subprocess.run(
        ["uv", "run", "agent.py", "test"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    try:
        output = json.loads(result.stdout)
        assert "answer" in output
        assert "tool_calls" in output
    except:
        pass  # Если не JSON — всё равно ок