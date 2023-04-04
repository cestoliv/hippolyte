# Using GPT4All

## Setup llama.cpp

To use GPT4All with Hippolyte, you will first need to setup [llama.cpp](https://github.com/ggerganov/llama.cpp) with a `GPT4All` model.

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```

Then, download the GPT4All ggml model into the `./models` folder.

To test that everything is working, try to run it:

```bash
./main --model ./models/gpt4all-lora-quantized.bin -n 256 --repeat_penalty 1 -t 8 -ins
# You whould be able to "chat" with GPT4All
```

## Setup Hippolyte

You will then need to configure Hippolyte to use GPT4All, to do so, add the following to your `.env` file.

(make sure to replace at least the values between <>)

*(Restart the app for the changes to take effect)*

```env
# GPT4All
GPT4ALL_ENABLED=True
GPT4ALL_PATH=<path/to/llama.cpp>
GPT4ALL_MODEL_PATH=<path/to/gpt4all-lora-quantized.bin>
GPT4ALL_KEEP_IN_MEMORY=True
```

**If you want GPT4All to keep a context of the conversations, and to get answers faster (especially if you are not using an SSD): set `GPT4ALL_KEEP_IN_MEMORY=False`**
