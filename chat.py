
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
from dotenv import load_dotenv

# local imports
from src.answer.base_answer import BaseAnswer
from src.functions import get_index, get_models
from openapi import check_openai_api_key


console = Console()

# Load environment variables
load_dotenv()
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME') or 'Hippolyte'
VERBOSE = os.getenv('VERBOSE', 'false').lower() == 'true'

# Load or create index
# index = None
# with console.status(Fore.BLUE + Style.BRIGHT + 'Loading index...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
# 	index = get_index()

# Load models
models: dict[str, BaseAnswer] = {}
with console.status(Fore.BLUE + Style.BRIGHT + 'Loading models...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
	models = get_models()

if len(models) == 0:
	print(Fore.RED + Style.BRIGHT + 'No models configured. Please check your configuration.' + Style.RESET_ALL)
	exit(1)
model: BaseAnswer = models[next(iter(models))]
model = models['llama2']

print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is ready!' + Style.RESET_ALL)

history = []

while True:
	text = input(
		'\n'
		+ Fore.LIGHTMAGENTA_EX
		+ ('[%s] ' % model.model['id'])
		+ Style.RESET_ALL
		+ Fore.GREEN + Style.BRIGHT + '> ' + Style.RESET_ALL
	)
	print()

	if text.strip() == '':
		continue
	if text.strip().lower() in ['exit', 'quit']:
		print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is shutting down...' + Style.RESET_ALL)
		break

	with console.status("", spinner='point', spinner_style='blue') as status:
		answer = model.answer(text, history=history)

		def escape_spaces_in_path(path: str) -> str:
			return path.replace(' ', '\\ ')

		# # print sources
		# if len(answer['context']) > 0:
		# 	console.print(Markdown('**Sources used:**\n'
		# 		+ '\n'.join(['- ' + '{0: <9}'.format("**" + str(round(source["similarity"] or 0, 3)) + "**") + '  ' + escape_spaces_in_path(source['path']) for source in answer['context']])
		# 	))
		# else:
		# 	console.print(Markdown('**No sources used.**'))
		# console.print()
		response = answer['answer']
		history.append({
			'user': text,
			'assistant': response
		})
	markdown = Markdown(str(response))
	console.print(markdown)
