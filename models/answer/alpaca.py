import subprocess

from models.answer.base import BaseAnswer
from models.index.base import BaseIndex

class AlpacaAnswer(BaseAnswer):
	def __init__(self, index: BaseIndex, alpaca_cpp_path: str):
		super().__init__('alpaca', index)

		# Local path to Alpaca C++ repo
		self.alpaca_cpp_path = alpaca_cpp_path

	# def create_prompt(self, query_text: str, context_text: str) -> str:
	# 	return (
	# 		'### Instruction:\n'
	# 		'We have provided context information below.\n'
	# 		"---------------------\n"
	# 		"{context_str}\n"
	# 		"---------------------\n"
	# 		"Given this information, please answer the following question as precisely as possible, with examples and code snippets when applicable.\n"
	# 		"### Input:\n"
	# 		"{query_str}\n"
	# 		"### Reponse:"
	# 	).format(
	# 		context_str=context_text,
	# 		query_str=query_text
	# 	)

	# def create_prompt(self, query_text: str, context_text: str) -> str:
	# 	return (
	# 		'We have provided context information below.\n'
	# 		"---------------------\n"
	# 		"{context_str}"
	# 		"\n---------------------\n"
	# 		"Given this information, please answer the following question as precisely as possible, with examples and code snippets when applicable.\n"
	# 		"---------------------\n"
	# 		"{query_str}"
	# 		"\n---------------------\n"
	# 		"Answer:"
	# 	).format(
	# 		context_str=context_text,
	# 		query_str=query_text
	# 	)

	# def get_prompt_template(self) -> str:
	# 	return (
	# 		'We have provided context information below.\n'
	# 		"---------------------\n"
	# 		"{context_str}\n"
	# 		"---------------------\n"
	# 		"Given the above information, please answer the following question.\n"
	# 		"Question: {query_str}\n"
	# 		"Answer:"
	# 	)

	def get_prompt_template_opinion(self) -> str:
		return (
			'Below is an instruction that describes a task. Write a response that appropriately completes the request.\n'
			'Instruction: Read the given information and answer the question.\n'
			'Bob said:\n'
			"---------------------\n"
			"{context_str}\n"
			"---------------------\n"
			"Question: {query_str} in Bob's opinion\n"
			"Answer:"
		)

	def get_prompt_template(self) -> str:
		return (
			'Below is an instruction that describes a task. Write a response that appropriately completes the request.\n'
			'Instruction: Read the given information and answer the question.\n'
			"---------------------\n"
			"{context_str}\n"
			"---------------------\n"
			"Question: {query_str} from the given information\n"
			"Answer:"
		)

	# def get_prompt_template(self) -> str:
	# 	return (
	# 		'Instruction: Read the given information and answer the question like if you where Bob.\n'
	# 		'Bob said:\n'
	# 		"---------------------\n"
	# 		"{context_str}"
	# 		"---------------------\n"
	# 		"Question: {query_str}\n"
	# 		"Answer:"
	# 	)

	def create_prompt(self, query: str, context: list[str]) -> str:
		return self.get_prompt_template().format(query_str=query, context_str='\n'.join(context))

	def answer(self, query: str, context: list[str] = None):
		if context is None:
			context = self.index.sources(query, 1)
		prompt = self.create_prompt(query, context)

		process = subprocess.Popen(
			[
				self.alpaca_cpp_path + 'main',
				'--seed', '-1',
				'--threads', '8',
				'--n_predict', '256',
				'--model', '/home/cestoliv/Downloads/llama.cpp/models/ggml-model-q4_0.bin.tmp',
				'--top_k', '40',
				'--top_p', '0.95',
				'--temp', '0.1',
				'--repeat_last_n', '64',
				'--repeat_penalty', '1.3',
				'-p', prompt
			],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		stdout, stderr = process.communicate()
		# TODO: check for errors

		# Remove prompt from response
		response = stdout.decode('utf-8')
		response = response.replace(prompt, '', 1).strip(' \n\n')
		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response,
		}
