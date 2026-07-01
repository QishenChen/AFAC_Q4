"""expand_query — Synonym expansion for financial terms.
Full implementation extracted from Retriever.expand_query.
"""

from agent.tools._loader import get_indices
from agent.tools._shared import _split_pipe_query


# Cached synonym group map
_synonym_groups = None


def _build_synonym_map() -> dict[str, set[str]]:
    """Build a term -> synonym-set map from config/financial_terms.json.

    If two canonical terms share a synonym, their groups are merged so the
    resulting set contains every connected term.
    """
    global _synonym_groups
    if _synonym_groups is not None:
        return _synonym_groups

    indices = get_indices()
    synonyms = indices["financial_terms"].get("synonyms", {})

    term_to_group = {}
    for canonical, syns in synonyms.items():
        group = set(syns)
        group.add(canonical)
        # Merge with any existing groups that overlap with this group
        merged = set(group)
        for term in group:
            if term in term_to_group:
                merged.update(term_to_group[term])
        for term in merged:
            term_to_group[term] = merged

    _synonym_groups = term_to_group
    return _synonym_groups


def expand_query_to_sets(query: str) -> dict[str, set[str]]:
    """Split a '|'-delimited query and map each term to its synonym set.

    Returns a dict {original_term: set(synonyms incl. itself)}.  Terms without
    known synonyms map to a singleton set containing only themselves.
    """
    term_to_group = _build_synonym_map()
    terms = _split_pipe_query(query)
    result = {}
    for term in terms:
        group = set(term_to_group.get(term, {term}))
        group.add(term)
        result[term] = group
    return result


def expand_query(query: str) -> str:
    """Backward-compatible '|'-joined expansion.

    Expands each term to its synonym set and re-joins with '|'.
    """
    sets = expand_query_to_sets(query)
    expanded = set()
    for term, group in sets.items():
        expanded.update(group)
    return "|".join(sorted(expanded))
