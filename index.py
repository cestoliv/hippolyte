# llama_index imports
from llama_index import GPTSimpleVectorIndex, LLMPredictor, download_loader

# langchain imports
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI

# cli imports
from colorama import Fore, Style

# local imports
from prompt import QA_PROMPT


ObsidianReader = None

def find_relevant_sources(query_text: str, index: GPTSimpleVectorIndex, top_k=5) -> str:
	relevant_sources = ''
	response = index.query(query_text, response_mode="no_text", text_qa_template=QA_PROMPT, similarity_top_k=top_k)
	sources = response.source_nodes
	for source in sources:
		relevant_sources += source.source_text + '\n'
	return relevant_sources

def get_llm(model: str) -> ChatOpenAI | OpenAI:
	if model == 'gpt-4' or model == 'gpt-3.5-turbo':
		return ChatOpenAI(temperature=0, model_name=model)
	elif model == 'text-davinci-003':
		return OpenAI(temperature=0, model_name=model)
	else:
		print(Fore.RED + Style.BRIGHT + 'Model not supported' + Style.RESET_ALL)
		exit(1)

def create_index(documents_path: str, save_path: str, model: str) -> GPTSimpleVectorIndex:
	if not ObsidianReader:
		ObsidianReader = download_loader('ObsidianReader')
	llm_predictor = LLMPredictor(llm=get_llm(model))

	documents = ObsidianReader(documents_path).load_data()

	# TODO: max_token
	index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor)
	index.save_to_disk(save_path)
	return index

def load_index(index_path: str, model: str) -> GPTSimpleVectorIndex:
	llm_predictor = LLMPredictor(llm=get_llm(model))
	index = GPTSimpleVectorIndex.load_from_disk(index_path, llm_predictor=llm_predictor)
	return index
