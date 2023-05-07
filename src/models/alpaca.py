from src.type import Model, LLamaModel

alpaca = Model(
	id="alpaca",
	name="Alpaca",
	context_size=2048,

	no_context_prompt=lambda query: (
		# Instructions
		'You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n'
		'Your answers use Markdown syntax.\n'
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request.\n'
		# # Example
		# '### Instruction:\n'
		# 'What is the capital of France?\n'
		# '### Response: The capital of France is Paris.\n'
		# Actual question
		'### Instruction:\n'
		"{query_str}\n"
		"### Response:"
	).format(query_str=query),

	context_prompt=lambda query, context: (
		# Instructions
		'You are Hippolyte, a linguistic AI model. You are in charge of answering questions.\n'
		'You must always answer using the given information.\n'
		'Your answers use Markdown syntax.\n'
		'Below is an instruction describing a task. Write a short, quick and informal answer that responds appropriately to the request using the given information.\n'
		# # Example
		# "### Instruction: Read the given information and answer the following question.\n"
		# "---------------------\n"
		# "Itritchi is a country. The capital of Itritchi is Aynesha.\n"
		# "---------------------\n"
		# "\n"
		# "### Input: What is the capital of Itritchi?\n"
		# "\n"
		# "### Response: The capital of Itritchi is Aynesha.\n"
		# Actual question
		"### Instruction: Read the given information and answer the following question.\n"
		"---------------------\n"
		"{context_str}\n"
		"---------------------\n"
		"\n"
		"### Input: {query_str}\n"
		"\n"
		"### Response:"
	).format(query_str=query, context_str='\n'.join(c["content"] for c in context)),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)

def getAlpaca_LlamaCpp(model_path: str) -> LLamaModel:
	return LLamaModel(
		id=alpaca["id"],
		name=alpaca["name"],
		context_size=alpaca["context_size"],
		no_context_prompt=alpaca["no_context_prompt"],
		context_prompt=alpaca["context_prompt"],
		clear_answer=alpaca["clear_answer"],

		model_path=model_path,
		stop_words=['### Instruction:', '### Output:', '### Input:'],
	)

