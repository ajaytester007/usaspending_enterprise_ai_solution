"""
MCP server placeholder.
Production path:
- expose refresh_dataset, query_gold_sql, get_metadata_catalog
- enforce tool allowlists and read-only query policy
- audit all calls
"""

def refresh_dataset(start_year: int, end_year: int, states: list[str]):
    return {'status': 'planned', 'start_year': start_year, 'end_year': end_year, 'states': states}

def get_metadata_catalog():
    return open('config/metadata_catalog.json', encoding='utf-8').read()
