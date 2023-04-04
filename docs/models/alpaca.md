# Using Alpaca

## Setup llama.cpp

To use Alpaca with Hippolyte, you will first need to setup [llama.cpp](https://github.com/ggerganov/llama.cpp) with an `Alpaca` model.

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```

Then, download the Alpaca ggml model into the `./models` folder.

To test that everything is working, try to run it:

```bash
./main --model ./models/ggml-alpaca-7b-q4.bin -n 256 --repeat_penalty 1 -t 8 -ins
# You whould be able to "chat" with Alpaca
```

## Setup Hippolyte

You will then need to configure Hippolyte to use Alpaca, to do so, add the following to your `.env` file.

*(Restart the app for the changes to take effect)*

```env
# Alpaca
ALPACA_ENABLED=True
ALPACA_PATH=<path/to/llama.cpp>
ALPACA_MODEL_PATH=<path/to/ggml-model-q4_0.bin>
ALPACA_KEEP_IN_MEMORY=False
```

**If you want Alpaca to keep a context of the conversations, and to get answers faster (especially if you are not using an SSD): set `ALPACA_KEEP_IN_MEMORY=False`**
