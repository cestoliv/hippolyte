import os
from colorama import Fore, Style

# llama_index imports
from llama_index import download_loader, SimpleDirectoryReader

# local imports
from src.answer.openai_api import OpenAIAnswer
from src.answer.llama_cpp import LLamaCppAnswer
from src.index.base_index import BaseIndex
from src.answer.base_answer import BaseAnswer
from src.index.rake_keyword_table_index import RAKEKeywordTableIndex
from src.index.simple_keyword_table_index import SimpleKeywordTableIndex
from src.index.vector_index import VectorIndex
from src.loaders.LogseqReader import LogseqReader

# models imports
from src.models.gpt35turbo import gpt35Turbo
from src.models.gpt4 import gpt4
from src.models.alpaca import getAlpaca_LlamaCpp
from src.models.gpt4all import getGpt4All_LlamaCpp
from src.models.vicuna import getVicuna_LlamaCpp
from src.models.openassistant import getOpenAssistant_LlamaCpp

from openapi import check_openai_api_key

# Take a dict of envname: type and check if they are set
def check_envs(envs: dict):
	for env, env_type in envs.items():
		os_env = os.getenv(env)
		if os_env is None:
			print(Fore.RED + Style.BRIGHT + f'{env} is not set' + Style.RESET_ALL)
			exit(1)
		if env_type == 'path' and not os.path.exists(os_env):
			print(Fore.RED + Style.BRIGHT + f'{env} is not a valid path' + Style.RESET_ALL)
			exit(1)
		if env_type == 'bool' and not os_env.lower() in ['true', 'false']:
			print(Fore.RED + Style.BRIGHT + f'{env} is not a valid boolean' + Style.RESET_ALL)
			exit(1)

def env_is_true(env: str):
	os_env = os.getenv(env)
	return os_env is not None and os_env.lower() == 'true'

# Function to get a dict of model based on .env
def get_models(index: BaseIndex) -> dict[str, BaseAnswer]:
	models: dict[str, BaseAnswer] = {}

	# GPT-3.5-turbo
	if env_is_true('GPT35T_ENABLED'):
		check_openai_api_key()
		models['gpt-3.5-turbo'] = OpenAIAnswer(gpt35Turbo, index)

	# GPT-4
	if env_is_true('GPT4_ENABLED'):
		check_openai_api_key()
		models['gpt-4'] = OpenAIAnswer(gpt4, index)

	# Alpaca
	if env_is_true('ALPACA_ENABLED'):
		check_envs({'ALPACA_MODEL_PATH': 'path'})
		models['alpaca'] = LLamaCppAnswer(getAlpaca_LlamaCpp(os.getenv('ALPACA_MODEL_PATH', '')), index)

	# GPT4All
	if env_is_true('GPT4ALL_ENABLED'):
		check_envs({'GPT4ALL_MODEL_PATH': 'path'})
		models['gpt4all'] = LLamaCppAnswer(getGpt4All_LlamaCpp(os.getenv('GPT4ALL_MODEL_PATH', '')), index)

	# Vicuna
	if env_is_true('VICUNA_ENABLED'):
		check_envs({'VICUNA_MODEL_PATH': 'path'})
		models['vicuna'] = LLamaCppAnswer(getVicuna_LlamaCpp(os.getenv('VICUNA_MODEL_PATH', '')), index)

	# OpenAssistant
	if env_is_true('OPENASSISTANT_ENABLED'):
		check_envs({'OPENASSISTANT_MODEL_PATH': 'path'})
		models['openassistant'] = LLamaCppAnswer(getOpenAssistant_LlamaCpp(os.getenv('OPENASSISTANT_MODEL_PATH', '')), index)

	return models

ObsidianReader = download_loader('ObsidianReader')
def get_index(documents_path: str = '') -> BaseIndex:
	if documents_path == '':
		check_envs({'DOCUMENTS_PATH': 'path'})
		documents_path = os.getenv('DOCUMENTS_PATH', '')

	# loader = ObsidianReader(documents_path)
	loader = LogseqReader(documents_path)
	# loader = SimpleDirectoryReader(documents_path, recursive=True, exclude_hidden=True)

	if os.getenv('INDEX') == 'vector_store':
		check_openai_api_key()
		return VectorIndex('text-embedding-ada-002', documents_path, loader)
	elif os.getenv('INDEX') == 'simple_keyword_table':
		return SimpleKeywordTableIndex(documents_path, loader)
	elif os.getenv('INDEX') == 'rake_keyword_table':
		return RAKEKeywordTableIndex(documents_path, loader)

	if not os.getenv('INDEX'):
		print(Fore.RED + Style.BRIGHT + f'INDEX is not set' + Style.RESET_ALL)
		exit(1)
	print(Fore.RED + Style.BRIGHT + f'INDEX {os.getenv("INDEX")} is not supported' + Style.RESET_ALL)
	exit(1)
