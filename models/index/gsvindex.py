import pathlib
import os
from colorama import Fore, Style
from llama_index import GPTSimpleVectorIndex, LLMPredictor
from langchain.chat_models import ChatOpenAI

# local imports
from models.index.base import BaseIndex

class GSVIndex(BaseIndex):

	# Loader id a llama_index BaseReader
	def __init__(self, model: str, documents_path: str, loader):
		super().__init__(model, documents_path, loader)

		self.index_path = 'indexes/index_GPTSimpleVectorIndex.json'

		if not pathlib.Path(self.index_path).exists():
			self.create_index()
		else:
			self.load_index()

	def create_index(self):
		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Creating index' + Style.RESET_ALL)

		# TODO: check openai api key
		llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'))

		# Create containing directory
		pathlib.Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
		documents = self.loader(self.documents_path).load_data()

		# Create index
		self.index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor)
		self.index.save_to_disk(self.index_path)

		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Index created' + Style.RESET_ALL)
		return self.index

	def load_index(self):
		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Loading index' + Style.RESET_ALL)

		# TODO: check openai api key
		llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'))

		# Load index
		self.index = GPTSimpleVectorIndex.load_from_disk(self.index_path, llm_predictor=llm_predictor)

		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Index loaded' + Style.RESET_ALL)
		return self.index

	def sources(self, query: str, top_k=5) -> list[str]:
		relevant_sources = []
		response = self.index.query(query, response_mode="no_text", similarity_top_k=top_k)
		sources = response.source_nodes
		for source in sources:
			relevant_sources.append(source.source_text)
		return relevant_sources
