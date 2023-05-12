from src.type import Model, LLamaModel

alpaca = Model(
	id="alpaca",
	name="Alpaca",
	context_size=2048,

	no_context_prompt=lambda query:
	(
		# Instructions
		'You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n'
		'Your answers use Markdown syntax.\n'
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request.\n'
		'### Instruction:\n'
		"{query_str}\n"
		"### Response:"
	).format(query_str=query),

	context_prompt=lambda query, context:
	(
		# Instructions
		'You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n'
		'You must always answer using the given information.\n'
		'Your answers use Markdown syntax.\n'
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request using the given information.\n'
		"### Instruction: Read the given information and answer the following question.\n"
		"---------------------\n"
		"{context_str}\n"
		"---------------------\n"
		"\n"
		"### Input: {query_str}\n"
		"\n"
		"### Response:"
	).format(query_str=query, context_str='\n'.join(c["content"] for c in context)),

	extractor_prompt=lambda query, context:
	(
		"{context}\n"
		"### Instruction: Extract in this text the information that could help (even if only partially) to answer this. Any information that is not directly related to the question should be excluded. If you do not find any related information, answer \"NONE\". Answer with a JSON object.\n"
		"Question: {query}\n"
		"### Response:"
	).format(query=query, context=context),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

def getAlpaca_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=alpaca["id"],
		name=alpaca["name"],
		context_size=alpaca["context_size"],
		no_context_prompt=alpaca["no_context_prompt"],
		context_prompt=alpaca["context_prompt"],
		extractor_prompt=alpaca["extractor_prompt"],
		clear_answer=alpaca["clear_answer"],

		model_path=model_path,
		stop_words=['### Instruction:', '### Output:', '### Input:', '### Response:'],
	)

