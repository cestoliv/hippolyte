import subprocess

from models.answer.base import BaseAnswer
from models.index.base import BaseIndex

class BloomAnswer(BaseAnswer):
	def __init__(self, index: BaseIndex, bloomz_cpp_path: str):
		super().__init__('bloom', index)

		# Local path to Bloom C++ repo
		self.bloomz_cpp_path = bloomz_cpp_path

	def get_prompt_template(self) -> str:
		return (
			'The following context will be used to answer the question.\n'
			"{context_str}\n\n"
			"Question: {query_str}\n"
			"Answer:"
		)

	def create_prompt(self, query: str, context: list[str]) -> str:
		return self.get_prompt_template().format(query_str=query, context_str='\n'.join(context))

	def answer(self, query: str, context: list[str] = None):
		if context is None:
			context = self.index.sources(query, 1)
		prompt = self.create_prompt(query, context)

		process = subprocess.Popen(
			[
				self.bloomz_cpp_path + 'main',
				'-t', '8',
				'-m', self.bloomz_cpp_path + 'models/ggml-model-bloomz-7b1-f16-q4_0.bin',
				'-n', '256',
				'-p', prompt
			],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		stdout, stderr = process.communicate()
		# TODO: check for errors

		response = stdout.decode('utf-8')
		# Remove first prompt
		response = response.replace(prompt, '', 1)
		# Remove everything before the second prompt
		response = response[response.find(prompt):]
		# Remove second prompt
		response = response.replace(prompt, '', 1)
		# Remove everything after '</s> [end of text]'
		response = response[:response.find('</s> [end of text]')]

		# Remove prompt from response (remove everything before the second question)
		#response = response.strip(' \n\n')[response.find('Question: ' + query):]
		# response = response.replace(prompt, '', 1).strip(' \n\n')
		return {
			'query': query,
			'context': context,
			'prompt': prompt,
			'answer': response,
		}
