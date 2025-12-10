
class Config:
    MODEL_NAME = 'gpt2'  # change to path/to/your/fine-tuned-model if available
    DEVICE = 'cuda' if __import__('torch').cuda.is_available() else 'cpu'
