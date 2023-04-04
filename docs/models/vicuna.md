# Using Vicuna

## Setup llama.cpp

To use Vicuna with Hippolyte, you will first need to setup [llama.cpp](https://github.com/ggerganov/llama.cpp) with a `Vicuna` model.

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```

Then, download the Vicuna ggml model into the `./models` folder.

To test that everything is working, try to run it:

```bash
./main --model ./models/ggml-vicuna-13b-4bit.bin -n 256 --repeat_penalty 1 -t 8 -ins
# You whould be able to "chat" with Vicuna
```

## Setup Hippolyte

You will then need to configure Hippolyte to use Vicuna, to do so, add the following to your `.env` file.

(make sure to replace at least the values between <>)

*(Restart the app for the changes to take effect)*

```env
# Vicuna
VICUNA_ENABLED=True
VICUNA_PATH=<path/to/llama.cpp>
VICUNA_MODEL_PATH=<path/to/ggml-vicuna-13b-4bit.bin>
VICUNA_KEEP_IN_MEMORY=False
```

**If you want Vicuna to keep a context of the conversations, and to get answers faster (especially if you are not using an SSD): set `VICUNA_KEEP_IN_MEMORY=False`**
