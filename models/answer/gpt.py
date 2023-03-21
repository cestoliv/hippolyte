from llama_index import QuestionAnswerPrompt
import openai
from models.answer.base import BaseAnswer
from models.index.base import BaseIndex


class GPTAnswer(BaseAnswer):
	def __init__(self, model: str, index: BaseIndex):
		super().__init__(model, index)

		# QA prompt
		self.qa_prompt = QuestionAnswerPrompt(self.get_prompt_template())

	def get_prompt_template(self) -> str:
		return (
			"We have provided context information below.\n"
			"---------------------\n"
			"{context_str}\n"
			"---------------------\n"
			"Given this information, please answer the following question. Format your answer in markdown.\n"
			"---------------------\n"
			"{query_str}\n"
			"---------------------\n"
		)

	def create_prompt(self, query: str, context: list[str]) -> str:
		return self.get_prompt_template().format(query_str=query, context_str='\n'.join(context))

	def answer(self, query: str, context: list[str] = None):
		if context is None:
			context = self.index.sources(query, 1)
		prompt = self.create_prompt(query, context)

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
