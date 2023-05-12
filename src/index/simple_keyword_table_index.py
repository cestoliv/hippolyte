import pathlib
import os
from colorama import Fore, Style

# llama_index imports
from llama_index import GPTSimpleKeywordTableIndex, StorageContext, load_index_from_storage # type: ignore
from llama_index.retrievers import KeywordTableSimpleRetriever # type: ignore

# local imports
from src.index.base_index import BaseIndex
from src.type import Source

class SimpleKeywordTableIndex(BaseIndex):

	# Loader id a llama_index BaseReader
	def __init__(self, documents_path: str, loader):
		super().__init__('', documents_path, loader)

		self.index_path = 'indexes/SimpleKeywordTable'

		if not pathlib.Path(self.index_path).exists():
			self.create_index()
		else:
			self.load_index()

	def create_index(self):
		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Creating index' + Style.RESET_ALL)

		# Create containing directory
		pathlib.Path(self.index_path).mkdir(parents=True, exist_ok=True)
		documents = self.loader.load_data()

		# Create index
		self.index = GPTSimpleKeywordTableIndex.from_documents(documents)
		self.index.storage_context.persist(persist_dir=self.index_path)

		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Index created' + Style.RESET_ALL)
		return self.index

	def load_index(self):
		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Loading index' + Style.RESET_ALL)

		# Load index
		storage_context = StorageContext.from_defaults(persist_dir=self.index_path)
		self.index = load_index_from_storage(storage_context)

		if os.environ.get('VERBOSE').lower() == 'true':
			print(Fore.BLUE + Style.BRIGHT + 'Index loaded' + Style.RESET_ALL)
		return self.index

	# Set top_k to -1 to get all sources
	def sources(self, query: str, top_k=-1) -> list[Source]:
		retriever = KeywordTableSimpleRetriever(index=self.index)

		relevant_sources: list[Source] = [] # {'content': str, 'similarity': float}
		sources = retriever.retrieve(query)
		for source in sources:
			if len(relevant_sources) >= top_k and top_k != -1:
				break

			path = None
			if source.node.extra_info is not None and 'path' in source.node.extra_info:
				path = source.node.extra_info['path']

			relevant_sources.append({
				'document_id': source.node.doc_id,
				'content': source.node.get_text(),
				'similarity': source.score,
				'path': path,
			})
		return relevant_sources
