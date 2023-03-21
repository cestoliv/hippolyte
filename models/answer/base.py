# local imports
from models.index.base import BaseIndex


class BaseAnswer:
	def __init__(self, model: str, index: BaseIndex):
		self.model = model
		self.index = index

	def get_prompt_template(self) -> str:
		raise NotImplementedError

	def create_prompt(self, query: str) -> str:
		raise NotImplementedError

	def answer(self, query: str):
		raise NotImplementedError
