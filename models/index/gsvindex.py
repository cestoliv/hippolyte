from llama_index import GPTSimpleVectorIndex, LLMPredictor, QuestionAnswerPrompt
from langchain.chat_models import ChatOpenAI

# local imports
from models.index.base import BaseIndex

class GSVIndex(BaseIndex):
	def __init__(self, model: str):
		super().__init__(model)

		# Load index
		llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'))
		self.index_path = 'indexes/index_GPTSimpleVectorIndex.json'
		self.index = GPTSimpleVectorIndex.load_from_disk(self.index_path, llm_predictor=llm_predictor)

	def sources(self, query: str, top_k=5) -> list[str]:
		relevant_sources = []
		response = self.index.query(query, response_mode="no_text", similarity_top_k=top_k)
		sources = response.source_nodes
		for source in sources:
			relevant_sources.append(source.source_text)
		return relevant_sources
