import subprocess
import os
import pexpect
from colorama import Fore, Style

from models.answer.base import BaseAnswer
from models.index.base import BaseIndex

class AlpacaAnswer(BaseAnswer):
	def __init__(self, index: BaseIndex, path: str, model_path: str, keep_in_memory: bool):
		super().__init__('Alpaca', 'alpaca', index)

		self.path = path
		self.model_path = model_path
		self.keep_in_memory = keep_in_memory

		# Alpaca process command
		self.command = [
			os.path.join(self.path, 'main'),
			'--model', self.model_path,
			'-n', '256',
			'--repeat_penalty', '1',
			'-t', '8',
			'--top_k', '40',
			'--top_p', '0.95',
			'--temp', '0.1',
			'--repeat_last_n', '64',
			'--repeat_penalty', '1.3',
		]

		if self.keep_in_memory is True:
			command = self.command + ['-ins']
			command = command + ['-p', '"Below is an instruction that describes a task. Write a response that appropriately completes the request."']

			if os.environ.get('VERBOSE').lower() == 'true':
				print(Fore.BLUE + Style.BRIGHT + 'Starting Alpaca' + Style.RESET_ALL)
			self.process = pexpect.spawn(' '.join(command))
			self._wait_for_prompt()
			if os.environ.get('VERBOSE').lower() == 'true':
				print(Fore.BLUE + Style.BRIGHT + 'Alpaca started' + Style.RESET_ALL)

	def _wait_for_prompt(self):
		self.process.expect('\n> ', timeout=None)

	def no_context_prompt(self, query: str) -> str:
		return query

	def context_prompt(self, query: str, context: list[str]) -> str:
		return (
			'Below is an instruction that describes a task. Write a response that appropriately completes the request.\n'
			'Instruction: Read the given information and answer the question.\n'
			"---------------------\n"
			"{context_str}\n"
			"---------------------\n"
			"Question: {query_str} from the given information\n"
			"Answer:"
		).format(query_str=query, context_str='\n'.join(context))

	def answer(self, query: str, context: list[str] = None, use_context: bool = False):
		if use_context:
			if context is None:
				context = self.index.sources(query, 1)
			prompt = self.context_prompt(query, context)
		else:
			context = []
			prompt = self.no_context_prompt(query)

		if self.keep_in_memory is True:
			# Send prompt to Alpaca process
			self.process.sendline(prompt)
			self._wait_for_prompt()
			response = self.process.before.decode('utf-8')
		else:
			command = self.command + ['-p', prompt]
			process = subprocess.Popen(
				command,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			stdout, stderr = process.communicate()

			if stderr and 'main: error:' in stderr.decode('utf-8'):
				print(Fore.RED + Style.BRIGHT + stderr.decode('utf-8') + Style.RESET_ALL)
			response = stdout.decode('utf-8')

		# Remove prompt from response
		response = response.replace(prompt, '', 1).strip(' \n\n')

		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response,
		}
