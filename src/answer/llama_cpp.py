from typing import List

from llama_cpp import Llama # type: ignore

# local imports
from src.answer.base_answer import BaseAnswer
from src.chunks import create_chunks
from src.type import Answer, LLamaModel, Source

class LLamaCppAnswer(BaseAnswer):
	def __init__(self, model: LLamaModel):
		super().__init__(model)

		self.stop_words = model['stop_words']
		self.llm = Llama(model['model_path'], n_ctx=model['context_size'], verbose=False)

	"""
		Directly query the model with the given prompt
	"""
	def query(self, prompt: str) -> str:
		output = self.llm(prompt, stop=self.stop_words, echo=False)
		response = ''
		if len(output['choices']) > 0:
			response = output['choices'][0]['text']
		response = self.model["clear_answer"](response)
		return response
