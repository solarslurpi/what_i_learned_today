sqimport marimo

__generated_with = "0.9.32"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Notebook Goal
        The goal of this notebook is to explore and document the steps required to build a minimum model context protocol (mcp) client that talks with a local sqlite mcp server.

        ## What is MCP?
        The Model Context Protocol (MCP) is an implementation of a Remote Procedure Call (RPC) API. It builds upon the foundational RPC concepts developed by Bruce Nelson at Xerox PARC in the early 1980s. While the core idea remains the same - allowing one computer to execute code on another - MCP brings this concept to current technologies.

        MCP applies current best practices, using JSON-RPC 2.0 for message formatting and Pydantic for type definition and validation. Through Pydantic's type system, MCP ensures safe, validated data exchange between client and server, providing a robust framework for remote tool execution.

        Just as traditional RPC operates over various network protocols (TCP/IP, NetBEUI, IPX/SPX), MCP is designed to work over different transport layers. Currently, it uses stdio for local process communication, with the capability to use HTML/SSE for web-based interactions.  Modern tools like `uv` and its extension `uvx` have made it remarkably simple to launch and manage local MCP server subprocesses, demonstrating how the surrounding ecosystem makes an MCP implementation even better.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Absolute Minimal MCP SQLite Client

        ## Core Requirements

        1. **Essential Messages Only**
               - Initialize message (required by protocol)
               - Direct SQL query message

        3. **Minimal Message Flow**
           ```
           Client                          Server
           ─────────────────────────────────────────
           1. Initialize ─────────────────►
                         ◄───────────────── Capabilities
           2. SQL Query ─────────────────► "SELECT * FROM products ORDER BY price DESC LIMIT 2"
                         ◄───────────────── Query Results
           ```

        4. **Example Response Format**
           ```json
           {
               "jsonrpc": "2.0",
               "id": "query_id",
               "result": {
                   "columns": ["id", "name", "price"],
                   "rows": [
                       [1, "Gaming Mouse", 89.99],
                       [2, "Mechanical Keyboard", 79.99]
                   ]
               }
           }
           ```
        _Note: This example assumes the products table exists and has Gaming Mouse as the most expensive item followed by Mechanical Keyboard._
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Install the SDK
        The first thing to do is to install the sdk: `uv pip install mcp`.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Configure Server Parameters
        Next, we configure server parameters.  When setting up the server parameters, the transport protocol is specified.  There are two options for transport protocols: 

            1. stdio- Standard input/output.  This is the simple text-based protocol used throughout the history of computing from Unix pipes to Python's `print()` and `input()` functions. It is ideal for when all processes are running on the same machine.

            2. HTTP with SSE - HTTP server with Server-Sent Events.  This method is commonly used by web applications. HTTP `POST` are used for client-to-server messages. SSE (Server-Sent Events) are used for server-to-client messages.
        """
    )
    return


@app.cell
def __():
    from mcp import StdioServerParameters

    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-sqlite", "--db-path", "test.db"]
    )
    return StdioServerParameters, server_params


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        The `StdioServerParameters` class configures how the MCP client launches and communicates with an MCP server via stdio. It takes `command` (the Python launcher you want to use - e.g.: `uvx`, `python`, `py`), args (a list containing the server module and its arguments like "--db-path"), and an optional environment dictionary. When the client starts, it launches this server as a subprocess and communicates with it through stdio.
        This example uses "uvx" from the uv framework to launch the MCP server.y managed while launching Python applications.

        This example uses Anthropic's `sqlite` MCP server.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Client Session Pattern from MCP Python SDK
        In the client example within the  [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), The MCP client uses Context Managers to establish and maintain server communication. The outer context creates stdio channels (write_stream like print() and read_stream like input()), which the inner context uses to maintain an active ClientSession. This session handles bidirectional JSON-RPC 2.0 message flow with the server until explicitly closed. The pattern ensures proper resource cleanup while leveraging stdio - the same robust process communication mechanism that Unix pipes have used for decades.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Implementing the MCP Client Session Pattern

        Following the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) example, we'll implement the same client session pattern:

        ```python
        async def run_mcp():
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Session operations here
        ```

        This implementation:

        * Creates `stdio` channels through the outer context manager
        * Establishes an active ClientSession with the inner context manager
        * Resources are automatically cleaned up when context managers exit
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        # The `ClientSession`

        `ClientSession` is a class provided by the MCP SDK that manages the lifecycle of a connection to an MCP server. It abstracts the details of sending and receiving JSON-RPC 2.0 messages over a stream.

        ## `initialize` Method

        The `initialize` method in `ClientSession` is responsible for setting up the initial communication with the server. Here's a typical flow:

        1. **Establish Connection**: The session uses the provided `read` and `write` streams to communicate with the server.
        2. **Send Initialization Request**: The `initialize` method sends a predefined JSON-RPC message to the server to start the session.
        3. **Handle Server Response**: It waits for a response from the server, which typically includes server capabilities and other session-related information.
        4. **Error Handling**: If the server doesn't respond within a specified timeout or returns an error, the method handles these scenarios gracefully.
        5. 
        ## Example Usage


        Here's a typical usage pattern for `ClientSession` and its `initialize` method:
        """
    )
    return


@app.cell
async def __(server_params):
    from mcp import ClientSession
    from mcp import stdio_client

    async def run_mcp():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                init_result = await session.initialize()
                if init_result:
                    print("Initialization successful:", init_result)
                else:
                    print("Initialization failed")
    await run_mcp()
    return ClientSession, run_mcp, stdio_client


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # MCP Server Tool Discovery

        Before sending SQL queries to the MCP server, we need to:

        1. **Initialize Connection** To establish a connection with the server, verify protocol compatibility, and get server capabilities.
        2. **Discover Available Tools** To get a list of the tools the server has available as well as their purpose and parameters.
        """
    )
    return


@app.cell
async def __(ClientSession, server_params, stdio_client):
    async def run_mcp_tools():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                init_result = await session.initialize()
                if init_result:
                    print("Initialization successful:", init_result)

                    # List available tools
                    tools = await session.list_tools()
                    print("\nAvailable Tools:", tools)
                else:
                    print("Initialization failed")

    await run_mcp_tools()
    return (run_mcp_tools,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        In our case, we found that the SQLite MCP server provides several tools:

        | Tool Name | Description | Required Properties |
        |-----------|-------------|-------------------|
        | `read-query` | Execute a SELECT query on the SQLite database | `{"query": "SELECT SQL query to execute"}` |
        | `write-query` | Execute an INSERT, UPDATE, or DELETE query on the SQLite database | `{"query": "SQL query to execute"}` |
        | `list-tables` | List all tables in the SQLite database | `{}` (no properties needed) |
        | `describe-table` | Get the schema information for a specific table | `{"table_name": "name of the table to describe"}` |
        | `create-table` | Create a new table in the SQLite database | `{"query": "CREATE TABLE SQL statement"}` |
        | `append-insight` | Add a business insight to the memo | `{"insight": "Business insight discovered from data analysis"}` |

        This information allows us to properly structure our SQL queries and use the correct tool for each operation.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Executing SQL Queries with MCP

        After discovering the available tools, let's use the `list-tables` tool to see what tables are in the database.
        """
    )
    return


@app.cell
async def __(ClientSession, server_params, stdio_client):
    async def run_mcp_list_tables():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                init_result = await session.initialize()
                if init_result:
                    # List all tables
                    tables_result = await session.call_tool(
                        "list-tables",
                        {}  # No properties needed for list-tables
                    )
                    print("\nAvailable Tables:", tables_result)
                else:
                    print("Initialization failed")

    await run_mcp_list_tables()
    return (run_mcp_list_tables,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ## Exploring the Products Table
        After discovering that we have a `products` table in our database, we can understand its structure by using the `describe_table` tool.
        """
    )
    return


@app.cell
async def __(ClientSession, server_params, stdio_client):
    async def run_mcp_describe_table():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                init_result = await session.initialize()
                if init_result:
                    # Describe the products table structure
                    schema_result = await session.call_tool(
                        "describe-table",
                        {"table_name": "products"}
                    )
                    print("\nProducts Table Schema:", schema_result)
                else:
                    print("Initialization failed")

    await run_mcp_describe_table()
    return (run_mcp_describe_table,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ### Products Table Schema

        The `products` table has the following structure:

        | Column ID (cid) | Name | Data Type | Not Null | Default Value | Primary Key |
        |----------------|------|-----------|----------|---------------|-------------|
        | 0 | id | INTEGER | No | None | Yes |
        | 1 | name | TEXT | No | None | No |
        | 2 | price | REAL | No | None | No |

        **Table Details:**

        - Primary Key: `id` (INTEGER)
        - Text Field: `name` for product names
        - Numeric Field: `price` for product pricing (REAL for decimal values)
        - All fields are nullable (notnull = 0)
        - No default values set for any fields
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Querying the Products Table

        Now that we understand the table structure, we can query the products data:


        **Query Plan:**

        1. Use the `read-query` tool
        2. Write a SELECT statement to retrieve product data
        3. Required Property: `{"query": "SELECT statement"}` 

        Let's execute a query to see what data is in our products table!
        """
    )
    return


@app.cell
async def __(ClientSession, server_params, stdio_client):
    async def run_mcp_query():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                init_result = await session.initialize()
                if init_result:
                    # Query the products table
                    query_result = await session.call_tool(
                        "read-query",
                        {
                            "query": "SELECT * FROM products ORDER BY price DESC LIMIT 5"
                        }
                    )
                    print("\nQuery Results:", query_result)
                else:
                    print("Initialization failed")

    await run_mcp_query()
    return (run_mcp_query,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Query Results: Top 5 Products by Price

        | ID | Name | Price |
        |----|------|-------|
        | 10 | Mini Drone | $299.99 |
        | 4 | Smart Watch | $199.99 |
        | 20 | Portable SSD | $179.99 |
        | 18 | Gaming Headset | $159.99 |
        | 12 | Keyboard | $129.99 |
        """
    )
    return


if __name__ == "__main__":
    app.run()
