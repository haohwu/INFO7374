import re
import streamlit as st
from openai import OpenAI
from prompts import get_system_prompt

st.title("☃️ Frosty")

# Initialize the chat messages history
client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            response += (delta.choices[0].delta.content or "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for SQL queries and execute if available
        sql_matches = re.findall(r"```sql\n(.*?)\n```", response, re.DOTALL)
        if sql_matches:
            conn = st.connection("snowflake")
            results = []
            for sql in sql_matches:
                # Split the SQL into separate statements
                statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
                for stmt in statements:
                    try:
                        result = conn.query(stmt)
                        if not result.empty:
                            results.append(result)
                    except Exception as e:
                        if f"{e}" != "Unknown error":
                            st.error(f"Error executing SQL: {e}")
            
            if results:
                message["results"] = results[-1]  # Store only the last result
                for result in results:
                    st.dataframe(result)
            
        st.session_state.messages.append(message)