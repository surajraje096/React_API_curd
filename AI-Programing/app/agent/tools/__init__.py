from typing import Callable, Dict, Any, List

TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    is_risky: bool = False,
    risk_level: str = "LOW"
):
    """Decorator or function to register agent tools with metadata."""
    def decorator(func: Callable):
        TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "is_risky": is_risky,
            "risk_level": risk_level,
            "func": func
        }
        return func
    return decorator


def get_openai_tool_definitions() -> List[Dict[str, Any]]:
    """Returns tool schemas in standard OpenAI Function Calling format."""
    definitions = []
    for tool_name, tool_data in TOOL_REGISTRY.items():
        definitions.append({
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_data["description"],
                "parameters": tool_data["parameters"]
            }
        })
    return definitions


# Import tool implementations to register them in TOOL_REGISTRY
from app.agent.tools import database_tools, risky_tools

__all__ = ["TOOL_REGISTRY", "register_tool", "get_openai_tool_definitions"]

