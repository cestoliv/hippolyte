# llama_index imports
from llama_index import QuestionAnswerPrompt

QA_PROMPT_TMPL = (
	"We have provided context information below. \n"
	"---------------------\n"
	"{context_str}"
	"\n---------------------\n"
	"Given this information, please answer the following question.\n"
	"---------------------\n"
	"{query_str}"
	"\n---------------------\n"
	"Answers as precisely as possible, with examples and code snippets when applicable. Format your answer in markdown. Start your answer with *Based on your personal knowledge*"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

def create_prompt(query_text: str, context_text: str) -> str:
	return QA_PROMPT_TMPL.format(
		context_str=context_text,
		query_str=query_text
	)
