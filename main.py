"""
MCP Server Template
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field

import mcp.types as types

mcp = FastMCP("Echo Server", stateless_http=True)


@mcp.tool(
    title="Echo Tool",
    description="Echo the input text",
)
def echo(text: str = Field(description="The text to echo")) -> str:
    return text

@mcp.tool(title="Magic Matrix", description="Calculate Magic Matrix")
def calculate_magic_matrix(in_param):
    import http.client
    import json

    # Input parameter for mymagic function
    # in_param = 5  # Default value as per function definition

    # Convert input parameter to stringified JSON
    parameters = json.dumps({
        "nargout": 1,        # mymagic returns one output
        "rhs": [in_param]    # Pass the input argument
    })

    # Send RESTful request to MPS
    conn = http.client.HTTPConnection("20.199.27.70:9910")
    headers = {"Content-Type": "application/json"}

    # Endpoint format: /<archive>/<function>
    conn.request("POST", "/MyProductionServerArchive/mymagic", parameters, headers)

    # Parse response
    response = conn.getresponse()
    result = response.read().decode("utf-8")
    return result


@mcp.resource(
    uri="greeting://{name}",
    description="Get a personalized greeting",
    name="Greeting Resource",
)
def get_greeting(
    name: str,
) -> str:
    return f"Hello, {name}!"


@mcp.prompt("")
def greet_user(
    name: str = Field(description="The name of the person to greet"),
    style: str = Field(description="The style of the greeting", default="friendly"),
) -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
