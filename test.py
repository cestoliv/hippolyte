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
from models.index.gsvindex import GSVIndex

load_dotenv()

if __name__ == '__main__':
	index = GSVIndex('text-embedding-ada-002')

	bench_questions = [
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
			'context': None
		},
		{
			'question': 'How to login as local user on windows ?',
			'context': None
		},
		{
			'question': 'Matrix, how to fix file not uploadind',
			'context': None
		},
	]

	models = {
		# 'gpt': GPTAnswer('gpt-3.5-turbo', index),
		'alpaca': AlpacaAnswer(index, '/home/cestoliv/Downloads/llama.cpp/'),
		# 'bloom': BloomAnswer(index, '/home/cestoliv/Downloads/bloomz.cpp/')
	}

	for question in bench_questions:
		print('Question: ' + question['question'])
		if question['context'] is None:
			print('Context: ' + '\n'.join(index.sources(question['question'], 1)))
		else:
			print('Context: ' + '\n'.join(question['context']))
		print()

		for model_name, model in models.items():
			print('\t Asking ' + model_name)
			print(model.answer(question['question'], question['context'])['answer'])
			print()
		print('----------------------------------------\n')
