TOOL_PERMISSIONS = {
    "planner": {
        "tools": set(),
    },
    "analyst": {
        "tools": {
            "finance",
            "calculator",
        },
    },
    "researcher": {
        "tools": {
            "tavily",
        },
    },
    "nemotron": {
        "tools": set(),
    },
    "validator": {
        "tools": {
            "calculator",
        },
    },
}


def is_tool_allowed(agent: str, tool: str) -> bool:
    """
    Check whether an agent is allowed to use a specific tool.
    """

    return tool in TOOL_PERMISSIONS.get(agent, {}).get(
        "tools",
        set(),
    )


def require_tool_permission(agent: str, tool: str) -> None:
    """
    Raise an error if an agent attempts to use
    a tool outside its permission boundary.
    """

    if not is_tool_allowed(agent, tool):
        raise PermissionError(
            f"Agent '{agent}' is not allowed to use "
            f"tool '{tool}'."
        )