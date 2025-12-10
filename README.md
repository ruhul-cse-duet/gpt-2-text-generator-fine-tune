
# GPT-2 Flask UI - Modularized project converted from notebook

This repository is an opinionated modular conversion of the uploaded notebook `gpt-2-text-generation-greedy-beam-search-finetun.ipynb` into a Flask web app + scripts.

## Structure
- `app/` - Flask app package and model loader
- `templates/` - Jinja2 templates for UI
- `static/` - CSS
- `scripts/` - training / data preparation scaffolds
- `run.py` - entrypoint for local development
- `Dockerfile` - container image
- `requirements.txt` - Python dependencies

## Quick start (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
# Open http://localhost:5000
```

## Notes
- The model loads the Hugging Face `gpt2` model by default. To use a fine-tuned model, update `app/config.py` MODEL_NAME to your model path.
- Training scaffold uses Hugging Face Trainer; edit `scripts/train.py` to point to your dataset.
