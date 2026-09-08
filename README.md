# DigiFarm MCP Server

This is my private MCP server for working with my DigiFarm poultry-management data. I built it with FastMCP, and I use Pydantic models to keep the data I send to my API consistent.

## What I Built

I use this server as the MCP layer between my tools and the DigiFarm services I own. It gives me one place to retrieve records and submit new records for:

- Flocks and flock feed-conversion data
- Egg production
- Expenses
- Health, feed, weight, and mortality logs
- Inventory items and inventory transactions
- Sales
- Users

The retrieval methods in `server.py` call my DigiFarm GET endpoints through `makeGetRequest`. The insertion methods serialize their Pydantic models and call my API through `makePostRequest`. `getUsers` is currently the exception because I read that data directly from my Supabase table.

## My MCP Tools

### Retrieval

`getFlocks`, `getFlockFCR`, `getEggProductionLogs`, `getExpenses`, `getHealthLogs`, `getFeedLogs`, `getWeightLogs`, `getMortalityLogs`, `getInventoryItems`, `getInventoryTransactions`, `getSales`, and `getUsers`.

### Insertion

`addNewFlock`, `addEggProductionLogs`, `addExpenseLogs`, `addHealthLog`, `addFeedLog`, `addWeightLog`, `addMortalityLog`, `addInventoryItem`, `addInventoryTransaction`, `addSalesLog`, and `addUser`.

## My Data Models

I keep the insertion payload definitions in `models.py`. The models cover flocks, egg production, expenses, health, feed, weight, mortality, inventory, sales, and users. Most records have optional database-generated IDs, while dates and resource-specific fields are defined by each model.

## Project Layout

- `main.py` creates my FastMCP instance and registers the tools.
- `server.py` contains my request helpers and DigiFarm tool methods.
- `models.py` contains my Pydantic request and response models.
- `requirements.txt` records the Python dependencies used by this environment.

I run the MCP entry point from this workspace with the FastMCP CLI:

```bash
fastmcp run main.py:mcp
```
