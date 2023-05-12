# local imports
from src.chunks import create_chunks
from src.index.base_index import BaseIndex
from src.type import Answer, Model, Source


class BaseAnswer:
	def __init__(self, model: Model):
		self.model = model

	"""
		Directly query the model with the given prompt
	"""
	def query(self, prompt: str) -> str:
		raise NotImplementedError

	"""
		Ask the model to extract the answer from the given context
		and return a new list of sources
	"""
	def extract(self, query: str, context: list[Source] = []) -> list[Source]:
		sources: list[Source] = []
		# print("Prompt length:", len(self.model["extractor_prompt"](query, '')))
		chunks = create_chunks(query, context, self.model)
		# print("Chunks:", len(chunks))

		for chunk in chunks:
			# print(self.model["extractor_prompt"](query, chunk['content']))
			extracted = self.query(self.model["extractor_prompt"](query, chunk['content']))

			# print("Extracted:", extracted)

			# TODO: make this a model function
			if extracted.startswith('NONE') or '"answer": "none"' in extracted.lower():
				continue

			sources.append({
				'content': extracted,
				'document_id': chunk['document_id'] + '_extracted',
				'path': chunk['path'],
				'similarity': chunk['similarity'],
			})

		return sources

	"""
		Ask the model to answer the query with the given context
		If the context is None, the no_context_prompt will be used
	"""
	def answer(self, query: str, context: list[Source] | None = None) -> Answer:
		prompt = ''
		if context is None:
			prompt = self.model['no_context_prompt'](query)
		else:
			prompt = self.model['context_prompt'](query, context)

		# Shrinking prompt to the lasts 4096 characters
		# TODO: improve this
		if len(prompt) > self.model['context_size']:
			prompt = prompt[-self.model['context_size']:]

		response = self.query(prompt)

		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response,
		}
