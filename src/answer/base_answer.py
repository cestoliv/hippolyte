# local imports
from src.index.base_index import BaseIndex
from src.type import Answer, Model, Source


class BaseAnswer:
	def __init__(self, model: Model, index: BaseIndex):
		self.model = model
		self.index = index

	def answer(self, query: str, context: list[Source] = [], use_context: bool = False, top_k: int = -1) -> Answer:
		raise NotImplementedError
