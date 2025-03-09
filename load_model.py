from transformers import AutoModel, AutoTokenizer

# Define model path
model_path = "C:/distilbert-base-uncased"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

print("Model loaded successfully!")
