# Start frontend

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file (make sure to replace at least the values between <>)

```env
OPENAI_API_KEY=<your openai api key>
GPT35T_ENABLED=True
```

**Run the frontend!**

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 3000
```

Go to [http://localhost:3000](http://localhost:3000)!

# Using different models

[Using GPT-4](models/gpt4.md)
[Using Alpaca](models/alpaca.md)
[Using GPT4All](models/gpt4all.md)
[Using Vicuna](models/vicuna.md)

// TODO: Using bloom
