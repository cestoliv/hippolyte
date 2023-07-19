from src.type import Model, LLamaModel

llama2 = Model(
	id="llama2",
	name="LLama2",
	context_size=4096,

	no_context_prompt=lambda query:
	(
		# Instructions
		'System: You are Hippolyte, a linguistic AI model. You are in charge of answering questions. '
		'Your answers uses Markdown syntax. '
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request.\n'
		"User: {query}\n"
		"Assistant: "
	).format(query=query),

	context_prompt=lambda query, context:
	(
		# Instructions
		'System: You are Hippolyte, a linguistic AI model. You are in charge of answering questions. '
		'You must always answer using the given information. '
		'Your answers use Markdown syntax. '
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request using the given information.\n'
		"User: Read the given information and answer the following question.\n"
		"----Informations----\n{context}\n"
		"----Question----\n{query}\n"
		"Assistant: "
	).format(query=query, context='\n'.join(c["content"] for c in context)),

	extractor_prompt=lambda query, context:
	(
		"System: You are an expert in information extraction.\n"
		"User: Extract in the given text the information that could help (even if only partially) to answer the given question. Any information that is not directly related to the question should be excluded. If you do not find any related information, answer \"NONE\". Answer with a JSON object.\n"
		"----Text----\n{context}\n"
		"----Question----\n{query}\n"
		"Assistant: "
	).format(query=query, context=context),

	history_prompt=lambda query, history:
	(
		"System: You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n"
		"{history_str}"
		"User: {query}\n"
		"Assistant: "
	).format(query=query, history_str='\n'.join([f"User: {h['user']}\nAssistant: {h['assistant']}\n" for h in history])),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

def getLlama2_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=llama2["id"],
		name=llama2["name"],
		context_size=llama2["context_size"],
		no_context_prompt=llama2["no_context_prompt"],
		context_prompt=llama2["context_prompt"],
		extractor_prompt=llama2["extractor_prompt"],
		history_prompt=llama2["history_prompt"],
		clear_answer=llama2["clear_answer"],

		model_path=model_path,
		stop_words=['System:', 'User:', 'Assistant:'],
	)

