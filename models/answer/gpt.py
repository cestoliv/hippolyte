import openai
from models.answer.base import BaseAnswer
from models.index.base import BaseIndex


class GPTAnswer(BaseAnswer):
	def __init__(self, model: str, index: BaseIndex, name: str):
		super().__init__(name, model, index)

	def no_context_prompt(self, query: str) -> str:
		return query

	def context_prompt(self, query: str, context: list[str]) -> str:
		return (
			"We have provided context information below.\n"
			"---------------------\n"
			"{context_str}\n"
			"---------------------\n"
			"Given this information, please answer the following question. Format your answer in markdown.\n"
			"---------------------\n"
			"{query_str}\n"
			"---------------------\n"
		).format(query_str=query, context_str='\n'.join(context))

	def answer(self, query: str, context: list[str] = None, use_context: bool = False):
		if use_context:
			if context is None:
				context = self.index.sources(query, 1)
			prompt = self.context_prompt(query, context)
		else:
			context = []
			prompt = self.no_context_prompt(query)

		response = openai.ChatCompletion.create(
			model = self.model,
			messages = [
				{ 'role': 'user', 'content': prompt },
			]
		)

		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response.choices[0].message.content.strip(' \n\t'),
		}
