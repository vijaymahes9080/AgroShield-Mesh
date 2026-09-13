"""
AgroShield Mesh - Model Context Protocol (MCP) Server
Exposes safe read-only and analytical tools over the Model Context Protocol.
"""

import sys
import json
from mcp_server.tools import (
    mcp_get_field_status,
    mcp_get_weather_summary,
    mcp_get_crop_calendar,
    mcp_search_agri_guidance,
    mcp_calculate_irrigation_need,
    mcp_generate_farmer_advisory
)

TOOLS_REGISTRY = {
    "get_field_status": mcp_get_field_status,
    "get_weather_summary": mcp_get_weather_summary,
    "get_crop_calendar": mcp_get_crop_calendar,
    "search_agri_guidance": mcp_search_agri_guidance,
    "calculate_irrigation_need": mcp_calculate_irrigation_need,
    "generate_farmer_advisory": mcp_generate_farmer_advisory
}


def handle_tool_call(name: str, arguments: dict) -> dict:
    """Dispatches tool call to registered handler with safety error catching."""
    if name not in TOOLS_REGISTRY:
        return {"error": f"Tool '{name}' not found in AgroShield safe tool registry."}
    try:
        func = TOOLS_REGISTRY[name]
        return func(**arguments)
    except Exception as e:
        return {"error": f"Execution error in tool '{name}': {str(e)}"}


def run_stdio_server():
    """Runs a standard JSON-RPC loop over standard input / standard output."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                tools_manifest = [
                    {
                        "name": "get_field_status",
                        "description": "Returns current field operational status, soil moisture, and latest risk level.",
                        "inputSchema": {"type": "object", "properties": {"field_id": {"type": "string"}}, "required": ["field_id"]}
                    },
                    {
                        "name": "get_weather_summary",
                        "description": "Returns weather observations and precipitation forecast.",
                        "inputSchema": {"type": "object", "properties": {"field_id": {"type": "string"}, "days": {"type": "integer"}}, "required": ["field_id"]}
                    },
                    {
                        "name": "get_crop_calendar",
                        "description": "Returns crop growth stage timeline and critical moisture thresholds.",
                        "inputSchema": {"type": "object", "properties": {"crop_name": {"type": "string"}, "stage": {"type": "string"}}}
                    },
                    {
                        "name": "search_agri_guidance",
                        "description": "Searches university agricultural guides (TNAU/ICAR) with verified citations.",
                        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "crop_name": {"type": "string"}, "language": {"type": "string"}}, "required": ["query"]}
                    },
                    {
                        "name": "calculate_irrigation_need",
                        "description": "Computes transparent deterministic irrigation urgency score (0-100).",
                        "inputSchema": {"type": "object", "properties": {"soil_moisture_pct": {"type": "number"}, "soil_type": {"type": "string"}, "crop_stage": {"type": "string"}, "forecast_rain_24h_mm": {"type": "number"}}}
                    },
                    {
                        "name": "generate_farmer_advisory",
                        "description": "Runs bounded agent workflow to produce evidence-grounded Tamil/English advisory.",
                        "inputSchema": {"type": "object", "properties": {"field_id": {"type": "string"}, "language": {"type": "string"}}, "required": ["field_id"]}
                    }
                ]
                res = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools_manifest}}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                result = handle_tool_call(name, args)
                res = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}}
            else:
                res = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}

            sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
