from src.type import Model, LLamaModel

gpt4all = Model(
	id="gpt4all",
	name="GPT4All",
	context_size=2048,

	no_context_prompt=lambda query: (
		'You are Hippolyte, an AI language model. You are tasked with answering questions.\n'
		'### Instruction:\n'
		"{query_str}\n"
		"### Response:"
	).format(query_str=query),

	context_prompt=lambda query, context: (
		'You are Hippolyte, an AI language model. You are tasked with answering questions using the given information.\n'
		"### Instruction: Read the given information and answer the following question.\n"
		"---------------------\n"
		"{context_str}\n"
		"---------------------\n"
		"\n"
		"### Input: {query_str}\n"
		"\n"
		"### Response:"
	).format(query_str=query, context_str='\n'.join([c['content'] for c in context])),

	extractor_prompt=lambda query, context:
	(
		"""Use the following pieces of context to find any informations that can help answering the question at the end. If you don't know the answer, just say "NONE", don't try to make up an answer. Make a bullet point list.

		{context}

		Question: {query}
		Helpful Answer:"""
	).format(query=query, context=context),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

def getGpt4All_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=gpt4all["id"],
		name=gpt4all["name"],
		context_size=gpt4all["context_size"],
		no_context_prompt=gpt4all["no_context_prompt"],
		context_prompt=gpt4all["context_prompt"],
		extractor_prompt=gpt4all["extractor_prompt"],
		clear_answer=gpt4all["clear_answer"],

		model_path=model_path,
		stop_words=[],
	)

