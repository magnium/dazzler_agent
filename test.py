from mistralai import Mistral
api_key = "DIiJ24tz6bS9ddYHBjRcCMc2kFwV17cs"
client = Mistral(api_key=api_key)
libraries = client.beta.libraries.list().data
for library in libraries:
    print(library.name, f"with {library.nb_documents} documents.")