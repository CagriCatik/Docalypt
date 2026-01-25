import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from docalypt.llm import LLMSettings, LLMError
from docalypt.documentation import DocumentGenerationRequest, generate_documentation
from docalypt.heading_splitting import split_by_headings

def test_heading_splitting_robustness(tmp_path):
    # Create a complex markdown structure
    content = """# Title 1
Text under 1
## Subtitle 1.1
Text under 1.1
# Title 2
Text under 2
"""
    input_file = tmp_path / "stream.md"
    input_file.write_text(content, encoding="utf-8")
    
    output_dir = tmp_path / "segments"
    chapters = split_by_headings(input_file, output_dir)
    
    assert len(chapters) == 3
    assert chapters[0]["title"] == "1. Title 1"
    assert chapters[1]["title"] == "2. Subtitle 1.1"
    assert chapters[2]["title"] == "3. Title 2"
    assert (output_dir / "01_title_1.md").exists()
    assert (output_dir / "02_subtitle_1_1.md").exists()
    assert (output_dir / "03_title_2.md").exists()

@patch("docalypt.llm.urlopen")
def test_full_generation_cycle(mock_urlopen, tmp_path):
    # Mock Ollama response
    mock_response = MagicMock()
    # Ollama returns multiple JSON lines
    mock_response.__enter__.return_value = [
        b'{"message": {"role": "assistant", "content": "Deep analysis "}, "done": false}',
        b'{"message": {"role": "assistant", "content": "complete."}, "done": true}'
    ]
    mock_urlopen.return_value = mock_response
    
    chapter_path = tmp_path / "chapter1.md"
    chapter_path.write_text("# Chapter 1\nContent data", encoding="utf-8")
    
    settings = LLMSettings(provider="ollama", model="qwen3")
    request = DocumentGenerationRequest(
        chapters=[chapter_path],
        settings=settings,
        prompt_template="Analyze {chapter_name}: {chapter_content}",
        destination_dirname="gen_test",
        standalone=False
    )
    
    result = generate_documentation(request)
    
    assert len(result.written) == 1
    dest_path = result.written[0][1]
    assert dest_path.name == "chapter1.docs.md"
    assert "Deep analysis complete." in dest_path.read_text()

def test_llm_settings_validation():
    with pytest.raises(LLMError, match="Unsupported provider"):
        settings = LLMSettings(provider="invalid")
        settings.normalized_provider()

def test_path_normalization_across_platforms():
    settings = LLMSettings(provider="ollama")
    # Simulate Windows path on backend
    from pathlib import PureWindowsPath
    p = PureWindowsPath("transcripts\\v1\\c1.md")
    # This is more of a logic check for our path handling strategy
    # We want posix style in the frontend/backend communication
    assert p.as_posix() == "transcripts/v1/c1.md"
