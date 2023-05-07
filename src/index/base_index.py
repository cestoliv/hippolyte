from src.type import Source


class BaseIndex:
	def __init__(self, model: str, documents_path: str, loader):
		self.model = model
		self.documents_path = documents_path
		self.loader = loader

	def create_index(self):
		raise NotImplementedError

	def load_index(self):
		raise NotImplementedError

	def sources(self, query: str, top_k: int = -1) -> list[Source]:
		raise NotImplementedError
