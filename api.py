# FastAPI
from fastapi import Body, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# other imports
from dotenv import load_dotenv

# local imports
from src.functions import get_index, get_models
from db import Database


load_dotenv()
app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins='*',
)

index = get_index()
models = get_models(index)

database = Database()


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
	return database.insert(query, model_name, answer['answer'], answer['context'], answer['prompt'])

@app.get("/api/v1/models/{model_name}/queries")
def get_queries(model_name: str):
	return database.get_queries(model_name)

app.mount("/", StaticFiles(directory="front/public", html=True), name="public")
