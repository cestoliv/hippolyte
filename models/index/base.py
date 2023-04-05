class BaseIndex:
	def __init__(self, model: str, documents_path: str, loader):
		self.model = model

	def create_index(self):
		raise NotImplementedError

	def load_index(self):
		raise NotImplementedError

	def sources(self, query: str) -> list[str]:
		raise NotImplementedError
