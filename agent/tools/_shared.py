"""
Shared helpers extracted from retriever.py — used by all search tools.
"""
# (no external deps needed for these pure helpers)


# Minimum fuzzy match score to consider a table/heading relevant
MIN_SCORE = 0.25


def _split_pipe_query(query: str) -> list[str]:
    """Split a pipe-delimited query into individual terms."""
    if "|" in query:
        return [t.strip() for t in query.split("|") if t.strip()]
    return [query]