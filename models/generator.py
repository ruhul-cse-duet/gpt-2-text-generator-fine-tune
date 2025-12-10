from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

MODEL_NAME = "gpt2"

# load once
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def _int_val(v, default):
    try:
        return int(v)
    except Exception:
        return default

def _float_val(v, default):
    try:
        return float(v)
    except Exception:
        return default


def generate(prompt, method="greedy", **params):
    """
    Returns only the continuation (prompt removed).
    method in ['greedy','beam','top_k','top_p']
    accepted params: max_length, num_return_sequences, top_k, top_p, temperature, num_beams
    """
    if not prompt:
        return "No prompt provided."

    # defaults & sanitization
    max_length = max(1, _int_val(params.get("max_length"), 100))
    try:
        max_allowed = tokenizer.model_max_length
    except Exception:
        max_allowed = 1024
    if max_length > max_allowed:
        max_length = max_allowed

    num_return_sequences = max(1, _int_val(params.get("num_return_sequences"), 1))
    top_k = max(0, _int_val(params.get("top_k"), 50))
    top_p = min(max(0.0, _float_val(params.get("top_p"), 0.9)), 1.0)
    temperature = max(0.01, _float_val(params.get("temperature"), 0.0))
    num_beams = max(1, _int_val(params.get("num_beams"), 5))

    # encode input and move to device
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # base kwargs
    gen_kwargs = {
        "input_ids": inputs,
        "max_length": max_length,
        "num_return_sequences": num_return_sequences,
        "pad_token_id": tokenizer.eos_token_id,  # avoid warning if prompt is long
    }

    # configure by method
    if method == "greedy":
        # deterministic single best continuation
        # greedy cannot reasonably produce multiple distinct sequences without sampling or beams.
        gen_kwargs.update({
            "do_sample": False,
            "no_repeat_ngram_size": 2
        })
        # enforce returning single sequence
        gen_kwargs["num_return_sequences"] = 1

    elif method == "beam":
        # beam search deterministic
        # ensure num_return_sequences <= num_beams (HuggingFace requirement)
        beams = max(2, num_beams)
        if num_return_sequences > beams:
            num_return_sequences = beams
        gen_kwargs.update({
            "do_sample": False,
            "num_beams": beams,
            "early_stopping": True,
            "num_return_sequences": num_return_sequences,
            "no_repeat_ngram_size" : 2
        })

    elif method == "top_k":
        gen_kwargs.update({
            "do_sample": True,
            "top_k": max(1, top_k),
            "temperature": temperature,
            # for clarity, do not pass top_p here (defaults to 1.0 inside HF)
        })
        # when sampling, it's okay to return multiple sequences

    elif method == "top_p":
        gen_kwargs.update({
            "do_sample": True,
            "top_p": top_p,
            "temperature": temperature,
        })

    else:
        return "Invalid method"

    # If sampling is enabled, avoid accidental beam args
    if gen_kwargs.get("do_sample", False):
        gen_kwargs.pop("num_beams", None)

    # Ensure num_return_sequences is reasonable (cap to 10 to avoid huge outputs)
    gen_kwargs["num_return_sequences"] = min(gen_kwargs.get("num_return_sequences", 1), 10)

    try:
        output_ids = model.generate(**gen_kwargs)
    except Exception as e:
        return f"Generation failed: {str(e)}"

    decoded = []
    # decode and strip prompt
    prompt_text = tokenizer.decode(inputs[0], skip_special_tokens=True)
    for seq in output_ids:
        text = tokenizer.decode(seq, skip_special_tokens=True)
        # if decoded starts with prompt_text, strip it
        if text.startswith(prompt_text):
            cont = text[len(prompt_text):].lstrip()
        else:
            # fallback: try raw prompt string (in case tokenization differences)
            if text.startswith(prompt):
                cont = text[len(prompt):].lstrip()
            else:
                # if prompt isn't present, return full text (defensive)
                cont = text
        decoded.append(cont)

    # join with HTML spacing (your template uses |safe)
    return "<br><br>".join(decoded)
