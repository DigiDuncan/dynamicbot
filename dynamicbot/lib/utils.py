def truncate(s, amount) -> str:
    """Return a string that is no longer than the amount specified."""
    if len(s) > amount:
        return s[:amount - 3] + "..."
    return s
