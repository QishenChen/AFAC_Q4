"""expand_query — Synonym expansion for financial terms.
Full implementation extracted from Retriever.expand_query.
"""

from agent.tools._loader import get_indices


def expand_query(query: str) -> str:
    """Expand query with financial synonyms from config/financial_terms.json."""
    indices = get_indices()
    financial_terms = indices["financial_terms"]
    synonyms = financial_terms.get("synonyms", {})
    expanded_terms = [query]
    for canonical, syns in synonyms.items():
        for syn in syns:
            if syn in query:
                expanded_terms.append(canonical)
                for other in syns:
                    if other not in query and other not in expanded_terms:
                        expanded_terms.append(other)
    return " ".join(expanded_terms)