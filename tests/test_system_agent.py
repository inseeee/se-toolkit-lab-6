import subprocess
import os

def test_agent_file_exists():
    """Test that agent.py exists"""
    assert os.path.exists("agent.py")

def test_agent_imports():
    """Test that agent imports without errors"""
    result = subprocess.run(
        ["uv", "run", "python", "-c", "import agent"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Import failed: {result.stderr}"