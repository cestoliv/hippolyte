from src.type import HugginFaceApiModel, Model, LLamaModel

openassistant = Model(
	id="openassistant",
	name="OpenAssistant",
	context_size=2048,

	no_context_prompt=lambda query: (
		'<|prompter|>'
		'You are Hippolyte, an AI language model. You are tasked with answering questions. Be concise and use markdown syntax.'
		'<|endoftext|><|assistant|>'
		'Ok, I will do my best to answer your question.'
		'<|endoftext|><|prompter|>'
		"{query_str}"
		'<|endoftext|><|assistant|>'
	).format(query_str=query),

	context_prompt=lambda query, context: (
		'<|prompter|>'
		'You are Hippolyte, an AI language model. You are tasked with answering questions using the given information. Be concise and use markdown syntax.'
		'<|endoftext|><|assistant|>'
		'Ok, I will do my best to answer your question, using the information you will provide.'
		'<|endoftext|><|prompter|>'
		"Information: \n"
		"---------------------\n"
		"{context_str}\n"
		"---------------------\n"
		"\n"
		"Question: {query_str}\n"
		'<|endoftext|><|assistant|>'
	).format(query_str=query, context_str='\n'.join([c['content'] for c in context])),

	extractor_prompt=lambda query, context:
	(
"""<|system|>Extract in the given document the informations that can help to answer the following question. Answer with a bullet list. Answer "NONE" if the document doesn't contains any related informations.<|endoftext|>
<|prompter|>
{query}
=====
{context}
=====
<|endoftext|>
<|assistant|>
"""

# """<|prompter|>Here is a series of dialogues between various people and an AI assistant specialized in summarization and information extraction. The job of the AI assistant is to extract from a document extract the information allowing to answer the user's question. The AI assistant does not answer the question, it simply gives sources in the form of a bullet list.<|endoftext|>

# <|prompter|>
# Question: Matrix, how to fix the file not uploading error?
# =====
# Document: type:: [[Documentation]]
# - # Matrix
# 	- ## Impossible d'Upload un fichier
# 		- `sudo chown -R 991:991 media_store/`
# =====
# <|endoftext|>
# <|assistant|>
# - sudo chown -R 991:991 media_store/
# <|endoftext|>

# <|prompter|>
# Question: What are the last books I read?
# =====
# Document: type:: [[Documentation]]
# - # Matrix
# 	- ## Impossible d'Upload un fichier
# 		- `sudo chown -R 991:991 media_store/`
# =====
# <|endoftext|>
# <|assistant|>
# NONE
# <|endoftext|>

# <|prompter|>
# Question: {query}
# =====
# Document: {context}
# =====
# <|endoftext|>
# <|assistant|>"""


		# "{context}\n"
		# "<|prompter|>"
		# "Extract in this text the information that could help (even if only partially) to answer this. Any information that is not directly related to the question should be excluded. If you do not find any related information, answer \"NONE\". Answer with a JSON object.\n"
		# "Question: {query}\n"
		# "<|endoftext|><|assistant|>"
	).format(query=query, context=context),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

openassistant_HuggingFaceApi = HugginFaceApiModel(
	id=openassistant["id"],
	name=openassistant["name"],
	context_size=openassistant["context_size"],
	no_context_prompt=openassistant["no_context_prompt"],
	context_prompt=openassistant["context_prompt"],
	extractor_prompt=openassistant["extractor_prompt"],
	clear_answer=openassistant["clear_answer"],

	# repo_id="OpenAssistant/stablelm-7b-sft-v7-epoch-3",
	repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
)

def getOpenAssistant_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=openassistant["id"],
		name=openassistant["name"],
		context_size=openassistant["context_size"],
		no_context_prompt=openassistant["no_context_prompt"],
		context_prompt=openassistant["context_prompt"],
		extractor_prompt=openassistant["extractor_prompt"],
		clear_answer=openassistant["clear_answer"],

		model_path=model_path,
		stop_words=['<|endoftext|>', '</|endoftext|>', '---------------------'],
	)


# Better extractor prompt, but too long
"""<|prompter|>Here is a series of dialogues between various people and an AI assistant specialized in summarization and information extraction. The job of the AI assistant is to extract from a document extract the information allowing to answer the user's question. The AI assistant does not answer the question, it simply gives sources in the form of a bullet list.<|endoftext|>

<|prompter|>
Question: What are the last books I read?
=====
Document: I read the book "The Lord of the Rings" by J. R. R. Tolkien. I also read the book "The Hobbit" by J. R. R. Tolkien. Before that, I read the book "The Silmarillion" by J. R. R. Tolkien. Now, I am reading the book "The Institute", by Stephen King.
=====
<|endoftext|>
<|assistant|>
- The Lord of the Rings, J. R. R. Tolkien
- The Hobbit, J. R. R. Tolkien
- The Silmarillion, J. R. R. Tolkien
- The Institute, Stephen King (currently reading)
<|endoftext|>

<|prompter|>
Question: Matrix, how to fix the file not uploading error?
=====
Document: type:: [[Documentation]]
- # Matrix
	- ## Impossible d'Upload un fichier
		- `sudo chown -R 991:991 media_store/`
=====
<|endoftext|>
<|assistant|>
- sudo chown -R 991:991 media_store/
<|endoftext|>

<|prompter|>
Question: Which book am I currently reading?
=====
Document: I read the book "The Lord of the Rings" by J. R. R. Tolkien. I also read the book "The Hobbit" by J. R. R. Tolkien. Before that, I read the book "The Silmarillion" by J. R. R. Tolkien. Now, I am reading the book "The Institute", by Stephen King.
=====
<|endoftext|>
<|assistant|>
- The Institute, Stephen King
<|endoftext|>

<|prompter|>
Question: The MSSQL service did not start on Windows Server. Help me fix it.
=====
Document: type:: [[Documentation]]
tags:: #sysadmin #windows

- # Troubleshooting
	- ## Service fail to start without logs
		- Start MSSQL from cli to try having more informations:
		  ```powershell
		  net start MSSQL$instancename
		  # net start MSSQL$EBP
		  ```
	- ## The service did not start due to a logon failure.
		- ### The MSSQL service log on as Administrator and the password has changed
		  id:: 63198c3c-8e45-4da2-80b9-0a9e4112b0a7
			- Open `Sql Server Configuration Manager` > `SQL Server Services`, right-click on `SQL Server (instancename)` > `Properties`.
			  Under `Log On`, change the account password.
			  Then, you can start the service, from cli, or from the Server Manager.
=====
<|endoftext|>
<|assistant|>
- Logon failure (the password has changed): Open `Sql Server Configuration Manager` > `SQL Server Services`, right-click on `SQL Server (instancename)` > `Properties` > `Log On`, change the account password.
<|endoftext|>


<|prompter|>
Question: {query}
=====
Document: {context}
=====
<|endoftext|>
<|assistant|>"""
