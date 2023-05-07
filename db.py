# SQL
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# For markdown to html
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import html

# other imports
import json

class Database:

	def __init__(self):
		engine = sqlalchemy.create_engine('sqlite:///queries.db')
		connection = engine.connect()
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.session.autocommit = True

		self.Query = sqlalchemy.Table('query', sqlalchemy.MetaData(),
			sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column('query', sqlalchemy.String),
			sqlalchemy.Column('model', sqlalchemy.String),
			sqlalchemy.Column('answer', sqlalchemy.String),
			sqlalchemy.Column('context', sqlalchemy.String), # A JSON serialized list of dicts {context: str, similarity: float}
			sqlalchemy.Column('prompt', sqlalchemy.String),
			sqlalchemy.Column('timestamp', sqlalchemy.DateTime, default=sqlalchemy.func.now())
		)
		# Create table if not exists
		self.Query.create(engine, checkfirst=True)

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

	def insert(self, query, model_name, answer, context, prompt):
		query = self.Query.insert().values(
			query=query,
			model=model_name,
			answer=answer,
			context=json.dumps(context),
			prompt=prompt
		)

		result = self.session.execute(query)
		return self.row_to_object(
			self.session.query(self.Query).filter_by(id=result.lastrowid).first()
		)

	def get_queries(self, model_name):
		queries = self.session.query(self.Query).filter(self.Query.c.model == model_name).all()
		return [self.row_to_object(query) for query in queries]
