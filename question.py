
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
index = None
with console.status(Fore.BLUE + Style.BRIGHT + 'Loading index...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
	index = get_index()

# Load models
models: dict[str, BaseAnswer] = {}
with console.status(Fore.BLUE + Style.BRIGHT + 'Loading models...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
	models = get_models()

if len(models) == 0:
	print(Fore.RED + Style.BRIGHT + 'No models configured. Please check your configuration.' + Style.RESET_ALL)
	exit(1)
model: BaseAnswer = models[next(iter(models))]

print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is ready!' + Style.RESET_ALL)

HELP = '''
- `exit` or `quit` => Say goodbye to %s
- `index` => Recreate the index (to take into account changes in your documents)
- `models` => List available models
- `model <model_name>` => Select a model
- `search` => Toggle search only mode (no answer generation)
''' % ASSISTANT_NAME

# Print menu
console.print(Markdown('''
You can start questioning %s.
Here are the available orders:
- `help` => Show this help
%s
''' % (ASSISTANT_NAME, HELP)))

searchOnly = False

while True:
	text = input(
		'\n'
		+ Fore.LIGHTMAGENTA_EX
		+ ('[search] ' if searchOnly else '[%s] ' % model.model['id'])
		+ Style.RESET_ALL
		+ Fore.GREEN + Style.BRIGHT + '> ' + Style.RESET_ALL
	)
	print()

	if text.strip() == '':
		continue
	elif text == "help":
		console.print(Markdown('Here are the available orders:\n%s' % HELP))
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
		continue
	elif text == "models":
		# List available models
		models_list = []
		for model_id in models.keys():
			line = '- `' + model_id + '`'
			if model_id == model.model['id']:
				line += ' *used*'
			models_list.append(line)

		console.print(Markdown('Available models:\n'
			+ '\n'.join(models_list)
			+ '\n'
		))
		continue
	elif text.startswith("model "):
		# Select a model
		model_id = text[6:]
		if model_id not in models:
			print(Fore.RED + Style.BRIGHT + 'Model ' + model_id + ' does not exist or is not configured.' + Style.RESET_ALL)
		else:
			model = models[model_id]
			print(Fore.BLUE + Style.BRIGHT + 'Model ' + model.model['name'] + ' selected.' + Style.RESET_ALL)
		continue
	elif text == "search":
		searchOnly = not searchOnly
		print(Fore.BLUE + Style.BRIGHT + 'Search only mode is now ' + ('enabled' if searchOnly else 'disabled') + '.' + Style.RESET_ALL)
		continue

	context = index.sources(text)

	if searchOnly:
		with console.status("", spinner='point', spinner_style='blue') as status:
			if len(context) == 0:
				print(Fore.YELLOW + Style.BRIGHT + 'No results.' + Style.RESET_ALL)
			else:
				for r in range(len(context)):
					print(Fore.CYAN + Style.BRIGHT + 'n°' + str(r+1) + Style.RESET_ALL + ' ' + context[r]['document_id'], end='')
					if context[r]['similarity']:
						print(Fore.CYAN + Style.BRIGHT + ' similarity: ' + str(round(context[r]['similarity'] or 0, 3)) + Style.RESET_ALL, end='')
					print()
					print(context[r]['content'])
					print()
	else:
		with console.status("", spinner='point', spinner_style='blue') as status:
			answer = model.answer(text, context)

			def escape_spaces_in_path(path: str) -> str:
				return path.replace(' ', '\\ ')

			# print sources
			if len(answer['context']) > 0:
				console.print(Markdown('**Sources used:**\n'
					+ '\n'.join(['- ' + '{0: <9}'.format("**" + str(round(source["similarity"] or 0, 3)) + "**") + '  ' + escape_spaces_in_path(source['path']) for source in answer['context']])
				))
			else:
				console.print(Markdown('**No sources used.**'))
			console.print()
			response = answer['answer']
		markdown = Markdown(str(response))
		console.print(markdown)
