import os
from pathlib import Path
from typing import Any, List

from langchain.docstore.document import Document as LCDocument
from llama_index.readers.base import BaseReader
from llama_index.readers.file.markdown_parser import MarkdownParser
from llama_index.readers.schema.base import Document


class LogseqReader(BaseReader):
	"""Utilities for loading data from an Obsidian Vault.
	Args:
		input_dir (str): Path to the vault.
	"""

	def __init__(self, input_dir: str):
		"""Init params."""
		self.input_dir = Path(input_dir)

	def load_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
		"""Load data from the input directory."""
		docs: List[Document] = []
		for (dirpath, dirnames, filenames) in os.walk(self.input_dir):
			dirnames[:] = [d for d in dirnames if not d.startswith(".")]
			for filename in filenames:
				if filename.endswith(".md"):
					filepath = os.path.join(dirpath, filename)
					content = MarkdownParser().parse_file(Path(filepath))

					# Add the filename as the title of the document.
					if isinstance(content, list):
						for c in content:
							# c = 'title:: ' + filename[:-3] + '\n' + c
							docs.append(Document(c, extra_info={'path': filepath}))
					else:
						# content = 'title:: ' + filename[:-3] + '\n' + content
						docs.append(Document(content, extra_info={'path': filepath}))

		return docs

	def load_langchain_documents(self, **load_kwargs: Any) -> List[LCDocument]:
		"""Load data in LangChain document format."""
		docs = self.load_data(**load_kwargs)
		return [d.to_langchain_format() for d in docs]
