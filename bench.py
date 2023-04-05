# LOGGING
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
# END LOGGING

from dotenv import load_dotenv
from pprint import pprint

from models.answer.alpaca import AlpacaAnswer
from models.answer.bloom import BloomAnswer
from models.answer.gpt import GPTAnswer
from models.answer.gpt4all import GPT4AllAnswer
from models.functions import get_index, get_models
from models.index.gsvindex import GSVIndex

load_dotenv()

if __name__ == '__main__':
	index = get_index()
	models = get_models(index)

	bench_questions = [
		{
			'question': 'Hello, who are you?',
			'context': None # Will not use context
		},
		{
			'question': 'What is the capital of France?',
			'context': ['France is a country. The capital of France is Paris.']
		},
		{
			'question': 'What is the capital of Itritchi?',
			'context': ['Itritchi is a country. The capital of Itritchi is Aynesha.']
		},
		{
			'question': 'Who is Elon Musk?',
			'context': ['Itritchi is a country. The capital of Itritchi is Aynesha.']
		},
		{
			'question': 'What are the latest books I\'ve read?',
			'context': ["Here is a list of the last books i read: L'Etranger, Albert Camus; L'Institut, Stephen King; L'intelligence artificielle n'existe pas, Luc Julia; The Motivation Myth, Jeff Haden"]
		},
		{
			'question': 'Make a list of the last books I\'ve read',
			'context': ["Here is a list of the last books i read", "- L'Etranger, Albert Camus", "- L'Institut, Stephen King", "- L'intelligence artificielle n'existe pas, Luc Julia", "- The Motivation Myth, Jeff Haden"]
		},
		{
			'question': 'Make a list of the last books I\'ve read',
			'context': [] # Will use the index
		},
		{
			'question': 'How to login as local user on windows ?',
			'context': [] # Will use the index
		},
		{
			'question': 'Matrix, how to fix file not uploadind',
			'context': [] # Will use the index
		},
	]

	for question in bench_questions:
		print('Question: ' + question['question'])
		if question['context'] is not None:
			if len(question['context']) > 0:
				print('Context: ' + '\n'.join(question['context']))
			else:
				print('Context: ' + '\n'.join(index.sources(question['question'], 1)))
		print()

		for model_name, model in models.items():
			print('\t Asking ' + model.name)

			context = None
			use_context = False
			if question['context'] is not None:
				if len(question['context']) > 0:
					context = question['context']
				use_context = True

			print(model.answer(question['question'], context, use_context=use_context)['answer'])
			print()
		print('----------------------------------------\n')
