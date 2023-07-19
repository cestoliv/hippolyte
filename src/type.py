from typing import Callable, Optional, TypedDict, List

class Source(TypedDict):
	document_id: str
	content: str
	similarity: float | None
	path: str | None

class Answer(TypedDict):
	query: str
	context: Optional[List[Source]]
	prompt: str
	answer: str

class Model(TypedDict):
	id: str
	name: str
	context_size: int

	no_context_prompt: Callable[[str], str]
	context_prompt: Callable[[str, List[Source]], str]
	extractor_prompt: Callable[[str, str], str]
	history_prompt: Callable[[str, List[str]], str]
	clear_answer: Callable[[str], str]

class LLamaModel(Model):
	model_path: str
	stop_words: List[str]

class HugginFaceApiModel(Model):
	repo_id: str
