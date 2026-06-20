"""
Backward-compatibility shim — re-exports from agent.tools package.
New code should import directly from agent.tools.
"""

from agent.tools import TOOLS, execute_tool, search_headings, search_tables, search_text, get_section, compute, expand_query, get_doc_info
