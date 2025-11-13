import streamlit as st
from mistralai import Mistral, MessageOutputEntry, ToolExecutionEntry

def message_output_entry_to_md(entry) -> str:
    md_parts = []
    refs = {} # title -> (index, description)
    for chunk in entry:
        if chunk.type == "text":
            md_parts.append(chunk.text.strip())
        elif chunk.type in "tool_reference":
            title = chunk.title.removesuffix(".pdf")
            if not title in refs:
                idx = len(refs)
                refs[title] = (idx, chunk)
            else:
                idx = refs[title][0]
            md_parts.append(f"[^{idx+1}]")
    for title, (idx, chunk) in refs.items(): # dict is sorted by insertion order
        url = f"({chunk.url})" if chunk.tool == "web_search" else ""
        md_parts.append(f"\n[^{idx+1}]: {title} *{chunk.description}*{url}\n")
    return "\n".join(md_parts)

client = Mistral(api_key="DIiJ24tz6bS9ddYHBjRcCMc2kFwV17cs")
model = "mistral-tiny"
agent = "ag_019a7d3d270770948f3bcb2e4a6f4a01"#"ag_019a783390427144bca557571b4c11e8"
st.title("Dazzler AI Agent")
user_input = st.text_input("Ask me anything about Dazzler:")
if user_input:
    response = client.beta.conversations.start(
        agent_id=agent,
        inputs=user_input
    )

    if isinstance(response.outputs[0], MessageOutputEntry):
        st.write(response.outputs[0].content)
    elif len(response.outputs) > 1 and isinstance(response.outputs[1], MessageOutputEntry):
        st.write(response.outputs[1].content)
    elif isinstance(response.outputs[0], ToolExecutionEntry):
        #html_output = message_output_entry_to_md(response)
        try:
            st.write(message_output_entry_to_md(response.outputs[1].content))
        except:
            st.write(response)

