from fastmcp import FastMCP
from server import DigiFarm

mcp=FastMCP("ShadowStrike")

mcp_app=mcp.http_app(
    allowed_hosts=["*"],
    allowed_origins=["*"],
    host_origin_protection=False,
)

digitools=DigiFarm()

mcp.tool(digitools.getFlocks,description="gets the flock data from digifarm database")
mcp.tool(digitools.getFlockFCR,description="gets the feed convertion ratio for the flock")
mcp.tool(digitools.getEggProductionLogs,description="Gets the egg production details")
mcp.tool(digitools.getHealthLogs,description="Gets the health logs")
mcp.tool(digitools.getFeedLogs,description="Gets the feed logs")
mcp.tool(digitools.getWeightLogs,description="Gets the weight logs")
mcp.tool(digitools.getMortalityLogs,description="Gets the mortality logs")
mcp.tool(digitools.getInventoryItems,description="Gets the inventory items")
mcp.tool(digitools.getInventoryTransactions,description="Gets the inventory transactions")
mcp.tool(digitools.getSales,description="Gets the sales logs")
mcp.tool(digitools.getUsers,description="Gets the users")
mcp.tool(digitools.addEggProductionLogs,description="Add egg production logs")
mcp.tool(digitools.addExpenseLogs,description="Add a single record of the Expense logs")
mcp.tool(digitools.addHealthLog,description="Add a health log")
mcp.tool(digitools.addFeedLog,description="Add a feed log")
mcp.tool(digitools.addWeightLog,description="Add a weight log")
mcp.tool(digitools.addMortalityLog,description="Add a mortality log")
mcp.tool(digitools.addInventoryItem,description="Add an inventory item")
mcp.tool(digitools.addInventoryTransaction,description="Add an inventory transaction")
mcp.tool(digitools.addSalesLog,description="Add a sales log")
mcp.tool(digitools.addUser,description="Add a user")
mcp.tool(digitools.getExpenses,description="Retrieves the expense logs from database")
mcp.tool(digitools.addNewFlock,description="allows registering a new batch of poultry")
mcp.tool(digitools.deleteWeightLog, description="Delete a weight log by id")
mcp.tool(digitools.deleteAllWeightLogs, description="Delete all weight logs")

