
# LOGGING
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
# END LOGGING

# cli imports
from rich.console import Console
from rich.markdown import Markdown

from colorama import Fore, Style

# other imports
import os
from os.path import exists
import readline
from dotenv import load_dotenv

# local imports
from models.answer.base import BaseAnswer
from models.functions import get_index, get_models
from openapi import check_openai_api_key


console = Console()

# Load environment variables
load_dotenv()
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME') or 'Hippolyte'
VERBOSE = os.getenv('VERBOSE').lower() == 'true'

DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH')

# Load or create index
index = None
with console.status(Fore.BLUE + Style.BRIGHT + 'Loading index...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
	index = get_index(DOCUMENTS_PATH)

# Load models
models = {}
with console.status(Fore.BLUE + Style.BRIGHT + 'Loading models...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
	models = get_models(index)

if len(models) == 0:
	print(Fore.RED + Style.BRIGHT + 'No models configured. Please check your configuration.' + Style.RESET_ALL)
	exit(1)
model: BaseAnswer = models[next(iter(models))]

print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is ready!' + Style.RESET_ALL)

# Print menu
console.print(Markdown('''
You can start questioning %s.
Here are the available orders:
- `exit` or `quit` => Say goodbye to %s
- `index` => Recreate the index (to take into account changes in your documents)
- `models` => List available models
- `model <model_name>` => Select a model
''' % (ASSISTANT_NAME, ASSISTANT_NAME)))


while True:
	print(Fore.GREEN + Style.BRIGHT)
	text = input("> ")
	print(Style.RESET_ALL)
	if text.strip() == '':
		continue
	elif text == "quit" or text == "exit":
		print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is shutting down...' + Style.RESET_ALL)
		break
	elif text == "index":
		# Ask for confirmation
		confirmation = input(Fore.YELLOW + Style.BRIGHT + 'Are you sure you want to re-create the index? This can be long and costly. [y/N] ' + Style.RESET_ALL)
		if confirmation.lower() == "y":
			# Re-create index
			with console.status(Fore.BLUE + Style.BRIGHT + 'Creating index (can take a lot of time)' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
				index.create_index()
	elif text == "models":
		# List available models
		models_list = []
		for model_name in models.keys():
			line = '- `' + model_name + '`'
			if model_name == model.model:
				line += ' *used*'
			models_list.append(line)

		console.print(Markdown('Available models:\n'
			+ '\n'.join(models_list)
			+ '\n'
		))
		continue
	elif text.startswith("model "):
		# Select a model
		model_name = text[6:]
		if model_name not in models:
			print(Fore.RED + Style.BRIGHT + 'Model ' + model_name + ' does not exist or is not configured.' + Style.RESET_ALL)
		else:
			model = models[model_name]
			print(Fore.BLUE + Style.BRIGHT + 'Model ' + model.model + ' selected.' + Style.RESET_ALL)
		continue

	response = ''
	with console.status("", spinner='point', spinner_style='blue') as status:
		answer = model.answer(text, use_context=True)
		response = answer['answer']

	markdown = Markdown(str(response))
	console.print(markdown)
