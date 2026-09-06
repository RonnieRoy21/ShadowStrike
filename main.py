from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

custom_middleware=[
    Middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)]

mcp=FastMCP("ShadowStrike")

app=mcp.http_app(middleware=custom_middleware)


@mcp.tool(name="activate or check in.",
         description="Before anything else happens,first request must be calling the name of the server to catch it's attention,it's like a passphrase")
def activateServer(name:str)->str:
    
    if name.startswith("ShadowStrike"):
        return "Go for Strike."
    return "Access denied."


    




