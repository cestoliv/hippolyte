# local imports
from models.index.base import BaseIndex


class BaseAnswer:
	def __init__(self, name: str, model: str, index: BaseIndex):
		self.name = name
		self.model = model
		self.index = index

	def no_context_prompt(self, query: str) -> str:
		raise NotImplementedError

	def context_prompt(self, query: str, context: list[str]) -> str:
		raise NotImplementedError

	def answer(self, query: str, context: list[str] = None, use_context: bool = False):
		raise NotImplementedError
