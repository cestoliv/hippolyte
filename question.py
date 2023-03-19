
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
import readline
from dotenv import load_dotenv
from os.path import exists

# local imports
from prompt import create_prompt, QA_PROMPT
from index import create_index, load_index


console = Console()

# Load environment variables
load_dotenv()
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME') or 'Hippolyte'
VERBOSE = os.getenv('VERBOSE') or False
MODEL = os.getenv('MODEL') or 'gpt-3.5-turbo'

if not os.getenv('OPENAI_API_KEY'):
	print(Fore.RED + Style.BRIGHT + 'No OPENAI_API_KEY found in .env file' + Style.RESET_ALL)
	exit(1)

DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH')
if not DOCUMENTS_PATH:
	print(Fore.RED + Style.BRIGHT + 'No DOCUMENTS_PATH found in .env file' + Style.RESET_ALL)
	exit(1)

# Set global variables
INDEX_PATH = 'indexes/index_GPTSimpleVectorIndex.json'

# Load or create index
index = None
if exists(INDEX_PATH):
	# Load from disk
	with console.status(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' loading...' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
		index = load_index(INDEX_PATH, MODEL)
else:
	# Create and save to disk
	with console.status(Fore.BLUE + Style.BRIGHT + 'Creating index (can take a lot of time)' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
		index = create_index(DOCUMENTS_PATH, INDEX_PATH, MODEL)

print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is ready!' + Style.RESET_ALL)


# Print menu
console.print(Markdown('''
You can start questioning %s.
Here are the available orders:
- `exit` or `quit` => Say goodbye to %s
- `index` => Recreate the index (to take into account changes in your documents)
''' % (ASSISTANT_NAME, ASSISTANT_NAME)))


while True:
	print(Fore.GREEN + Style.BRIGHT)
	text = input("> ")
	print(Style.RESET_ALL)
	if text == "quit" or text == "exit":
		print(Fore.BLUE + Style.BRIGHT + ASSISTANT_NAME + ' is shutting down...' + Style.RESET_ALL)
		break
	elif text == "index":
		# Ask for confirmation
		confirmation = input(Fore.YELLOW + Style.BRIGHT + 'Are you sure you want to re-create the index? This can be long and costly. [y/N] ' + Style.RESET_ALL)
		if confirmation.lower() == "y":
			# Re-create index
			with console.status(Fore.BLUE + Style.BRIGHT + 'Creating index (can take a lot of time)' + Style.RESET_ALL, spinner='bouncingBar', spinner_style='blue') as status:
				index = create_index(DOCUMENTS_PATH, INDEX_PATH, MODEL)

	response = ''
	with console.status("", spinner='point', spinner_style='blue') as status:
		response = index.query(text, text_qa_template=QA_PROMPT)

	# To see the prompt:
	# print(create_prompt(text, find_relevant_sources(text, index, top_k=1)))

	markdown = Markdown(str(response))

	print(Fore.BLUE + Style.BRIGHT + '< ' + ASSISTANT_NAME + Style.RESET_ALL)
	console.print(markdown)
