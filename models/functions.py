import os
from colorama import Fore, Style

# llama_index imports
from llama_index import download_loader

# local imports
from models.answer.alpaca import AlpacaAnswer
from models.answer.gpt import GPTAnswer
from models.answer.gpt4all import GPT4AllAnswer
from models.answer.vicuna import VicunaAnswer

from models.index.base import BaseIndex
from models.index.gsvindex import GSVIndex

# Take a dict of envname: type and check if they are set
def check_envs(envs: dict):
	for env, env_type in envs.items():
		if os.getenv(env) is None:
			print(Fore.RED + Style.BRIGHT + f'{env} is not set' + Style.RESET_ALL)
			exit(1)
		if env_type == 'path' and not os.path.exists(os.getenv(env)):
			print(Fore.RED + Style.BRIGHT + f'{env} is not a valid path' + Style.RESET_ALL)
			exit(1)
		if env_type == 'bool' and not os.getenv(env).lower() in ['true', 'false']:
			print(Fore.RED + Style.BRIGHT + f'{env} is not a valid boolean' + Style.RESET_ALL)
			exit(1)

def env_is_true(env: str):
	return os.getenv(env) is not None and os.getenv(env).lower() == 'true'

# Function to get a dict of model based on .env
def get_models(index: BaseIndex) -> dict:
	models = {}

	# GPT-3.5-turbo
	if env_is_true('GPT35T_ENABLED'):
		# TODO: check openai key
		models['gpt-3.5-turbo'] = GPTAnswer(index=index, model='gpt-3.5-turbo', name="GPT-3.5-turbo")

	# GPT-4
	if env_is_true('GPT4_ENABLED'):
		# TODO: check openai key
		models['gpt-4'] = GPTAnswer(index=index, model='gpt-4', name="GPT-4")

	# Alpaca
	if env_is_true('ALPACA_ENABLED'):
		check_envs({'ALPACA_PATH': 'path', 'ALPACA_MODEL_PATH': 'path', 'ALPACA_KEEP_IN_MEMORY': 'bool'})
		models['alpaca'] = AlpacaAnswer(
			index=index,
			path=os.getenv('ALPACA_PATH'),
			model_path=os.getenv('ALPACA_MODEL_PATH'),
			keep_in_memory=os.getenv('ALPACA_KEEP_IN_MEMORY').lower() == 'true'
		)

	# GPT4All
	if env_is_true('GPT4ALL_ENABLED'):
		check_envs({'GPT4ALL_PATH': 'path', 'GPT4ALL_MODEL_PATH': 'path', 'GPT4ALL_KEEP_IN_MEMORY': 'bool'})
		models['gpt4all'] = GPT4AllAnswer(
			index=index,
			path=os.getenv('GPT4ALL_PATH'),
			model_path=os.getenv('GPT4ALL_MODEL_PATH'),
			keep_in_memory=os.getenv('GPT4ALL_KEEP_IN_MEMORY').lower() == 'true'
		)

	# Vicuna
	if env_is_true('VICUNA_ENABLED'):
		check_envs({'VICUNA_PATH': 'path', 'VICUNA_MODEL_PATH': 'path', 'VICUNA_KEEP_IN_MEMORY': 'bool'})
		models['vicuna'] = VicunaAnswer(
			index=index,
			path=os.getenv('VICUNA_PATH'),
			model_path=os.getenv('VICUNA_MODEL_PATH'),
			keep_in_memory=os.getenv('VICUNA_KEEP_IN_MEMORY').lower() == 'true'
		)

	return models

ObsidianReader = download_loader('ObsidianReader')
def get_index(documents_path: str = None) -> BaseIndex:
	if not documents_path:
		documents_path = os.getenv('DOCUMENTS_PATH')

	if os.getenv('INDEX') == 'gpt_single_vector':
		return GSVIndex('text-embedding-ada-002', documents_path, ObsidianReader)

	if not os.getenv('INDEX'):
		print(Fore.RED + Style.BRIGHT + f'INDEX is not set' + Style.RESET_ALL)
		exit(1)
	print(Fore.RED + Style.BRIGHT + f'INDEX {os.getenv("INDEX")} is not supported' + Style.RESET_ALL)
	exit(1)
