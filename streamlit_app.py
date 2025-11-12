import streamlit as st
from mistralai import Mistral, MessageOutputEntry, ToolExecutionEntry

def message_output_entry_to_md(entry) -> str:
    md_parts = []
    refs = {} # title -> (index, description)
    for chunk in entry:
        if chunk.type == "text":
            md_parts.append(chunk.text.strip())
        elif chunk.type == "tool_reference":
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
agent = "ag_019a791e38bd722a97c8d2f6222204aa"#"ag_019a783390427144bca557571b4c11e8"
st.title("Dazzler AI Agent")
user_input = st.text_input("Ask me anything about Dazzler:")
if user_input:
    response = client.beta.conversations.start(
        agent_id=agent,
        inputs=user_input
    )

    if isinstance(response.outputs[0], MessageOutputEntry):
        st.write(response.outputs[0].content)
    elif isinstance(response.outputs[0], ToolExecutionEntry):
        #html_output = message_output_entry_to_md(response)
        st.write(message_output_entry_to_md(response.outputs[1].content))

