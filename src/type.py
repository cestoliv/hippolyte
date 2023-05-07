from typing import Callable, TypedDict, List

class Source(TypedDict):
	document_id: str
	content: str
	similarity: float

class Answer(TypedDict):
	query: str
	context: List[Source]
	prompt: str
	answer: str

class Model(TypedDict):
	id: str
	name: str
	context_size: int

	no_context_prompt: Callable[[str], str]
	context_prompt: Callable[[str, List[Source]], str]
	clear_answer: Callable[[str], str]

class LLamaModel(Model):
	model_path: str
	stop_words: List[str]
