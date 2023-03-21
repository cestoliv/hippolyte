class BaseIndex:
	def __init__(self, model: str):
		self.model = model

	def sources(self, query: str) -> list[str]:
		raise NotImplementedError
