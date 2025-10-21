import re

def extract_json_from_response(content: str) -> str:
    """Extract JSON from LLM response, handling Markdown code blocks."""
    # Match JSON object within triple backticks (with optional 'json' label)
    pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback: Strip leading/trailing whitespace and assume raw JSON
    stripped = content.strip().strip('\'"')
    if stripped.startswith('{') and stripped.endswith('}'):
        return stripped
    
    raise ValueError(f"No valid JSON found in response: {content[:200]} {content[-100:]}")
