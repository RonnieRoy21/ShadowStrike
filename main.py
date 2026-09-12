from fastmcp import FastMCP
from server import DigiFarm

mcp=FastMCP("ShadowStrike")

mcp_app=mcp.http_app(
    allowed_hosts=["*"],
    allowed_origins=["*"],
    host_origin_protection=False,
)

digitools=DigiFarm()


mcp.tool(digitools.EggProductionLogs,description="Manage egg production logs")
mcp.tool(digitools.ExpenseLogs,description="Manage expense logs")
mcp.tool(digitools.HealthLog,description="Manage health logs")
mcp.tool(digitools.FeedLog,description="Manage feed logs")
mcp.tool(digitools.WeightLog,description="Manage weight logs")
mcp.tool(digitools.MortalityLog,description="Manage mortality logs")
mcp.tool(digitools.InventoryItemLog,description="Manage inventory items")
mcp.tool(digitools.InventoryTransactionLog,description="Manage inventory transactions")
mcp.tool(digitools.SalesLog,description="Manage sales logs")
mcp.tool(digitools.Flock,description="Manage poultry flocks")
mcp.tool(digitools.getFlockFCR,description="Gets the fcr data on the flock")

