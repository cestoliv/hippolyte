from typing import List

from llama_cpp import Llama # type: ignore

# local imports
from src.answer.base_answer import BaseAnswer
from src.index.base_index import BaseIndex
from src.type import Answer, LLamaModel, Source

class LLamaCppAnswer(BaseAnswer):
	def __init__(self, model: LLamaModel, index: BaseIndex):
		super().__init__(model, index)

		self.stop_words = model['stop_words']
		self.llm = Llama(model['model_path'], n_ctx=model['context_size'], verbose=False)

	def answer(self, query: str, context: List[Source] = [], use_context: bool = False, top_k: int = -1) -> Answer:
		if use_context:
			if context is None:
				if top_k < 0:
					context = self.index.sources(query)
				else:
					context = self.index.sources(query, top_k=top_k)
			prompt = self.model["context_prompt"](query, context)
		else:
			context = []
			prompt = self.model["no_context_prompt"](query)

		if len(prompt) > self.model["context_size"]:
			prompt = prompt[-self.model["context_size"]:]

		output = self.llm(prompt, stop=self.stop_words, echo=False)
		response = ''
		if len(output['choices']) > 0:
			response = output['choices'][0]['text']
		response = self.model["clear_answer"](response)

		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response,
		}
