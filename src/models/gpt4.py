from src.type import Model, LLamaModel

gpt4 = Model(
	id="gpt-4",
	name="GPT 4",
	context_size=8192,

	no_context_prompt=lambda query: (
		'You are Hippolyte, an AI language model. You are tasked with answering questions.\n'
		'Question:\n'
		"{query_str}\n"
		'Answer:'
	).format(query_str=query),

	context_prompt=lambda query, context: (
		'You are Hippolyte, an AI language model. You are tasked with answering questions using the given information.\n'
		"We have provided context information below.\n"
		"---------------------\n"
		"{context_str}\n"
		"---------------------\n"
		"Given this information, please answer the following question. Format your answer in markdown.\n"
		"---------------------\n"
		"{query_str}\n"
		"---------------------\n"
	).format(query_str=query, context_str='\n'.join([c['content'] for c in context])),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)
