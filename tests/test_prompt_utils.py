
import pytest
from pathlib import Path
from processdesignagents.agents.utils.prompt_utils import load_prompt

def test_load_prompt_success():
    """Test loading a valid prompt file."""
    content = load_prompt("test_prompt.txt")
    assert content == "This is a test prompt."

def test_load_prompt_not_found():
    """Test loading a non-existent prompt file."""
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_prompt.txt")
