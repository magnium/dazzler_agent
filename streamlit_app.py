import streamlit as st
from mistralai import Mistral

client = Mistral(api_key="DIiJ24tz6bS9ddYHBjRcCMc2kFwV17cs")
agent = "ag_019a789fcbc37673b376c974ba2cc120"#"ag_019a783390427144bca557571b4c11e8"
st.title("Dazzler AI Agent")
user_input = st.text_input("Ask me anything about Dazzler:")
if user_input:
    response = client.beta.conversations.start(
        agent_id=agent,
        inputs=user_input
    )
    if response.outputs:
        st.write(response.outputs[0].content)
    else:
        st.write("No response from the agent.")
