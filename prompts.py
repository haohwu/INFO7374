import streamlit as st

DATABASE = "SNOWFLAKE_SAMPLE_DATA"
SCHEMA_PATH = st.secrets.get("SCHEMA_PATH", DATABASE)
TABLE_DESCRIPTION = """
This is the TPC-DS dataset in the SNOWFLAKE_SAMPLE_DATA database, which simulates the decision support system of a retail product supplier.
It includes various interconnected tables representing different aspects of the retail business,
such as sales, returns, inventory, and customer information across different sales channels
(store, catalog, and web). The data is available in two schemas: TPCDS_SF10TCL and TPCDS_SF100TCL.
"""

METADATA_QUERY = f"""
SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE 
FROM {SCHEMA_PATH}.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA IN ('TPCDS_SF10TCL')
ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
"""

GEN_SQL = """
You are an AI Snowflake SQL Expert named Frosty.
Your goal is to provide correct, executable SQL queries to users based on the TPC-DS dataset in the SNOWFLAKE_SAMPLE_DATA database.
You will be replying to users who expect responses in the character of Frosty.
The available tables, their schemas, and columns are provided in the <tables> tag.

{context}

Here are 8 critical rules for the interaction you must abide by:
<rules>
1. You MUST wrap the generated SQL code within ``` sql code markdown in this format:
```sql
USE DATABASE SNOWFLAKE_SAMPLE_DATA;
SELECT column1, column2 FROM schema.table WHERE condition
```
2. If not specified otherwise, LIMIT the number of results to 10.
3. Use ILIKE with wildcards for fuzzy text matching, e.g., ILIKE '%keyword%'
4. Generate a single Snowflake SQL query, not multiple.
5. Only use the tables and columns provided in the <tables> section.
6. Do not start column names with numbers.
7. Always include the schema name (TPCDS_SF10TCL) when referencing tables in your queries.
8. Always start your SQL queries with 'USE DATABASE SNOWFLAKE_SAMPLE_DATA;' to ensure the correct database is selected.
</rules>

For each user question, include a SQL query in your response.

To start, please introduce yourself briefly, describe the TPC-DS dataset at a high level,
and provide 3 example questions using bullet points that showcase the dataset's capabilities (Must use very easy examples that require small computation, because the datasets are large).
"""

@st.cache_data(show_spinner="Loading Frosty's context...")
def get_table_context(schema_path: str, table_description: str, metadata_query: str):
    conn = st.connection("snowflake")
    metadata = conn.query(metadata_query, show_spinner=False)
    
    tables = {}
    for _, row in metadata.iterrows():
        schema_table = f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
        if schema_table not in tables:
            tables[schema_table] = []
        tables[schema_table].append(f"**{row['COLUMN_NAME']}**: {row['DATA_TYPE']}")

    print(f"Number of tables: {len(tables)}")
    context = f"""
<database>{DATABASE}</database>

<schemaPath>{schema_path}</schemaPath>

<tableDescription>{table_description}</tableDescription>

<tables>
"""
    
    for schema_table, columns in tables.items():
        context += f"\n{schema_table}:\n" + "\n".join(columns) + "\n"
    
    context += "</tables>"
    return context

def get_system_prompt():
    table_context = get_table_context(
        schema_path=SCHEMA_PATH,
        table_description=TABLE_DESCRIPTION,
        metadata_query=METADATA_QUERY
    )
    return GEN_SQL.format(context=table_context)

# Streamlit app to view the initial system prompt
if __name__ == "__main__":
    st.header("System prompt for Frosty (TPC-DS Version with Database and Schema)")
    st.markdown(get_system_prompt())