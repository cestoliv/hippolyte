from colorama import Fore, Style
import openai
import time

# local imports
from src.answer.base_answer import BaseAnswer
from src.chunks import create_chunks
from src.type import Answer, Model, Source


class OpenAIAnswer(BaseAnswer):
	def __init__(self, model: Model):
		super().__init__(model)
		# TODO: check api key

	"""
		Directly query the model with the given prompt
	"""
	def query(self, prompt: str) -> str:
		while True:
			try:
				response = openai.ChatCompletion.create(
					model = self.model['id'],
					messages = [
						{ 'role': 'user', 'content': prompt },
					]
				)
				response = self.model['clear_answer'](response.choices[0].message.content)
				return response
			except openai.error.RateLimitError as e:
				print(Fore.YELLOW + "RateLimitError, retrying in 30 seconds..." + Style.RESET_ALL)
				time.sleep(30)
			except Exception as e:
				print(Fore.YELLOW + "Unknown error, retrying in 30 seconds..." + Style.RESET_ALL)
				time.sleep(30)
