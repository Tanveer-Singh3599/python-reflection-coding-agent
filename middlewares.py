from langchain.agents.middleware import (
    AgentMiddleware,
    ToolCallRequest,
    wrap_tool_call
)
from langchain.messages import ToolMessage

# tool middlewares
class CustomToolMiddlewares(AgentMiddleware):
    pass

class ToolErrorMiddleware(CustomToolMiddlewares):

    def wrap_tool_call(self, request: ToolCallRequest, handler) -> ToolMessage:
        # tool fallback
        try:
            return handler(request)
        except Exception as e:
            return ToolMessage(content=f"Error occured while tool execution. {e}.", tool_call_id = request.tool_call["id"])

# model middlewares
class CustomModelMiddlewares(AgentMiddleware):
    pass
