import openai

# local imports
from src.answer.base_answer import BaseAnswer
from src.index.base_index import BaseIndex
from src.type import Answer, Model, Source


class OpenAIAnswer(BaseAnswer):
	def __init__(self, model: Model, index: BaseIndex):
		super().__init__(model, index)

	def answer(self, query: str, context: list[Source] = [], use_context: bool = False, top_k: int = -1) -> Answer:
		if use_context:
			if context is None:
				if top_k < 0:
					context = self.index.sources(query)
				else:
					context = self.index.sources(query, top_k=top_k)
			prompt = self.model['context_prompt'](query, context)
		else:
			context = []
			prompt = self.model['no_context_prompt'](query)

		# Shrinking prompt to the lasts 4096 characters
		if len(prompt) > self.model['context_size']:
			prompt = prompt[-self.model['context_size']:]

		response = openai.ChatCompletion.create(
			model = self.model['id'],
			messages = [
				{ 'role': 'user', 'content': prompt },
			]
		)
		response = self.model['clear_answer'](response.choices[0].message.content)

		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response,
		}
