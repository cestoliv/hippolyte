from src.type import Model, Source

gpt35Turbo = Model(
	id="gpt-3.5-turbo",
	name="GPT 3.5 Turbo",
	context_size=4096,

	no_context_prompt=lambda query:
	(
		'You are Hippolyte, an AI language model. You are tasked with answering questions.\n'
		'Question:\n'
		"{query}\n"
		'Answer:'
	).format(query=query),

	context_prompt=lambda query, context:
	(
		"You are Hippolyte, an AI language model. You are tasked with answering questions using the given information. "
		"Note that the given information can be in any language. This information has been extracted from my personal notes. "
		"If you cannot answer using the sources below, say it and explain why the given information are not relevant. "
		"Format your answer in markdown.\n"
		"###\n"
		"Question: {query}\n"
		"Sources: \n"
		"---------------------\n"
		"{context}\n"
		"---------------------\n"
		"Answer: "
	).format(query=query, context='\n-----\n'.join([c['content'] for c in context])),

	extractor_prompt=lambda query, context:
	(
		"{context}\n"
		"This text is an extract from the user's personal notes. Extract in this text the information that could help (even if only partially) to answer this. Any information that is not directly related to the question should be excluded. If you do not find any related information, answer \"NONE\". Answer with a JSON object.\n"
		"### Question: {query}"
	).format(query=query, context=context),

	clear_answer=lambda answer: answer.strip(' \n\t'),
)
