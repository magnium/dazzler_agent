from mistralai import Mistral
api_key = "DIiJ24tz6bS9ddYHBjRcCMc2kFwV17cs"
client = Mistral(api_key=api_key)
library_agent = client.beta.agents.create(
    model="mistral-medium-latest",
    name="Dazzler AI agent",
    description="Agent used to access documents from the Dazzler library.",
    instructions="Answer questions about properties and usage of Dazzler (AOPDF, Acousto-optic programmable dispersive filter). Exclude all results related to Comic books or weapons. Use https://amplitude-laser.com/products/femtosecond-lasers/instrumentation-lasers-femtosecondes/dazzler/ for additional information.",
    tools=[{"type": "document_library", "library_ids": 
            ["019a77b0-594c-740d-ac5d-d5d8531479c1"]}],
    completion_args={
        "temperature": 0.3,
        "top_p": 0.95,
    }
)
print(library_agent)