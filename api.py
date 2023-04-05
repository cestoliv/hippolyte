from typing import Union
from fastapi import Body, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

# For markdown to html
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import html

# Local imports
from models.answer.alpaca import AlpacaAnswer
from models.answer.bloom import BloomAnswer
from models.functions import get_models
from models.answer.gpt import GPTAnswer
from models.answer.gpt4all import GPT4AllAnswer
from models.answer.vicuna import VicunaAnswer
from models.index.gsvindex import GSVIndex


load_dotenv()
app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins='*',
)


index = GSVIndex('text-embedding-ada-002')
models = get_models(index)

engine = sqlalchemy.create_engine('sqlite:///queries.db')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
session.autocommit = True

Query = sqlalchemy.Table('query', sqlalchemy.MetaData(),
	sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
	sqlalchemy.Column('query', sqlalchemy.String),
	sqlalchemy.Column('model', sqlalchemy.String),
	sqlalchemy.Column('answer', sqlalchemy.String),
	sqlalchemy.Column('context', sqlalchemy.String), # A JSON serialized list of strings
	sqlalchemy.Column('prompt', sqlalchemy.String),
	sqlalchemy.Column('timestamp', sqlalchemy.DateTime, default=sqlalchemy.func.now())
)
# Create table if not exists
Query.create(engine, checkfirst=True)

def row_to_object(row):
	class HighlightRenderer(mistune.HTMLRenderer):
		def block_code(self, code, info=None):
			if info:
				try:
					lexer = get_lexer_by_name(info, stripall=True)
					formatter = html.HtmlFormatter()
					return highlight(code, lexer, formatter)
				except:
					try:
						lexer = guess_lexer(code)
						formatter = html.HtmlFormatter()
						return highlight(code, lexer, formatter)
					except:
						return '<pre><code>' + mistune.escape(code) + '</code></pre>'
			else:
				try:
					lexer = guess_lexer(code)
					formatter = html.HtmlFormatter()
					return highlight(code, lexer, formatter)
				except:
					return '<pre><code>' + mistune.escape(code) + '</code></pre>'

	markdown = mistune.create_markdown(renderer=HighlightRenderer())

	return {
		'query': row.query,
		'answer': row.answer,
		'answer_html': markdown(row.answer),
		'context': json.loads(row.context),
		'prompt': row.prompt,
		'timestamp': row.timestamp,
	}


@app.get("/api/v1/contacts")
def get_contacts():
	# Loop in models and return a list of dicts
	contacts = []
	for model in models:
		contacts.append({
			"name": models[model].name,
			"model": models[model].model,
			"endpoint": f"/api/v1/models/{models[model].model}",
			"picture": "/imgs/profile-user.svg"
		})
	return contacts

@app.post("/api/v1/models/{model_name}")
def get_answer(model_name: str, query: str = Body(..., embed=True), use_context: bool = Body(..., embed=True)):
	if model_name not in models:
		return {"error": "Model not found"}

	answer = models[model_name].answer(query, use_context=use_context)

	# Save query
	query = Query.insert().values(
		query=answer['query'],
		model=model_name,
		answer=answer['answer'],
		context=json.dumps(answer['context']),
		prompt=answer['prompt']
	)

	result = session.execute(query)
	return row_to_object(
		session.query(Query).filter_by(id=result.lastrowid).first()
	)

@app.get("/api/v1/models/{model_name}/queries")
def get_queries(model_name: str):
	queries = session.query(Query).filter(Query.c.model == model_name).all()
	return [row_to_object(query) for query in queries]

app.mount("/", StaticFiles(directory="front/public", html=True), name="public")
