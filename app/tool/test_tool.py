from app.tool.base import BaseTool


_TEST_TOOL_DESCRIPTION = """A simple test tool that echoes the input and provides basic feedback.
Use this tool to test the planning flow and agent execution."""


class TestTool(BaseTool):
    name: str = "test_tool"
    description: str = _TEST_TOOL_DESCRIPTION
    parameters: dict = {
        "type": "object",
        "properties": {
            "input_text": {
                "type": "string",
                "description": "The text to process and echo back.",
            },
            "action": {
                "type": "string",
                "description": "The action to perform (echo, analyze, or summarize).",
                "enum": ["echo", "analyze", "summarize"],
                "default": "echo"
            }
        },
        "required": ["input_text"],
    }

    async def execute(self, input_text: str, action: str = "echo") -> str:
        """Execute the test tool with the given input and action"""
        
        if action == "echo":
            return f"Test Tool Echo: {input_text}"
        elif action == "analyze":
            word_count = len(input_text.split())
            char_count = len(input_text)
            return f"Analysis of '{input_text}': {word_count} words, {char_count} characters"
        elif action == "summarize":
            if len(input_text) > 50:
                return f"Summary: {input_text[:50]}..."
            else:
                return f"Summary: {input_text}"
        else:
            return f"Unknown action '{action}'. Echoing: {input_text}" 