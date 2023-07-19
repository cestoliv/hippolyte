from typing import List
import requests
import os
import time
from colorama import Fore, Style

# local imports
from src.answer.base_answer import BaseAnswer
from src.type import Answer, HugginFaceApiModel, Model, Source

class HuggingFaceApiAnswer(BaseAnswer):
	def __init__(self, model: HugginFaceApiModel):
		super().__init__(model)
		# TODO: check api key

		self.repo_id = model['repo_id']

	"""
		Directly query the model with the given prompt
	"""
	def query(self, prompt: str) -> str:
		API_URL = "https://api-inference.huggingface.co/models/" + self.repo_id
		headers = {"Authorization": "Bearer " + (os.getenv("HUGGINGFACE_API_KEY") or '')}

		while True:
			response = requests.post(API_URL, headers=headers, json={
				"inputs": prompt,
				"parameters": {
					"max_new_tokens": 1024,
					"temperature": 0.1,
					"repetition_penalty": 1.2,
					"top_p": 0.95,
					"top_k": 50,
				},
			})
			if response.status_code == 503:
				print(Fore.YELLOW + "Model is not ready yet, retrying..." + Style.RESET_ALL)
				time.sleep(30)
			else:
				response = response.json()
				break

		response = response[0]['generated_text']
		# Remove prompt
		response = response[len(prompt):]
		response = self.model["clear_answer"](response)

		# print(len(response))

		return response
