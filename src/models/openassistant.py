from src.type import Model, LLamaModel

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

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

def getOpenAssistant_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=openassistant["id"],
		name=openassistant["name"],
		context_size=openassistant["context_size"],
		no_context_prompt=openassistant["no_context_prompt"],
		context_prompt=openassistant["context_prompt"],
		clear_answer=openassistant["clear_answer"],

		model_path=model_path,
		stop_words=['<|endoftext|>', '</|endoftext|>', '---------------------'],
	)

