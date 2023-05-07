from src.type import Model, LLamaModel

vicuna = Model(
	id="vicuna",
	name="Vicuna",
	context_size=2048,

	no_context_prompt=lambda query: (
		'You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n'
		'Your answers use Markdown syntax.\n'
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request.\n'
		"### Human: {query_str}\n"
		"### Assistant:"
	).format(query_str=query),

	context_prompt=lambda query, context: (
		'You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n'
		'You must always answer using the given information.\n'
		'Your answers use Markdown syntax.\n'
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request using the given information.\n'
		"### Human: Read the given information and answer the following question.\n"
		"---------------------\n"
		"{context_str}\n"
		"---------------------\n"
		"Question: {query_str}\n"
		"\n"
		"### Assistant:"
	).format(query_str=query, context_str='\n'.join([c['content'] for c in context])),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

def getVicuna_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=vicuna["id"],
		name=vicuna["name"],
		context_size=vicuna["context_size"],
		no_context_prompt=vicuna["no_context_prompt"],
		context_prompt=vicuna["context_prompt"],
		clear_answer=vicuna["clear_answer"],

		model_path=model_path,
		stop_words=['### Human:'],
	)

