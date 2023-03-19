# cli imports
from colorama import Fore, Style

# other imports
import os
import requests

def check_openai_api_key(openai_api_key: str):
	if not os.getenv('OPENAI_API_KEY'):
		print(Fore.RED + Style.BRIGHT + 'No OPENAI_API_KEY found in .env file' + Style.RESET_ALL)
		exit(1)

	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + openai_api_key,
	}

	json_data = {
		'model': 'text-davinci-003',
		'prompt': 'test',
		'max_tokens': 1,
		'temperature': 0,
	}

	response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)
	if response.status_code != 200:
		print(Fore.RED + Style.BRIGHT + 'Invalid OPENAI_API_KEY' + Style.RESET_ALL)
		exit(1)
