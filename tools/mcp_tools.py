def tool_router(action, input):
    if action == "sql":
        from database.mysql import run_query
        return run_query(input)
    elif action == "search":
        return f"Searching {input}"