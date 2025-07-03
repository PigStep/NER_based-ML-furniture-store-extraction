from fastapi import FastAPI
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch

model_path = "product_model_ner"

# Load model and tokenizer
model = AutoModelForTokenClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
app = FastAPI()

@app.post("/predict")
async def predict_entities(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)[0]
    
    # formatting output
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    entities = [
        {"token": token, "label": model.config.id2label[pred.item()]}
        for token, pred in zip(tokens, predictions)
    ]
    return {"text": text, "entities": entities}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Открыт для локальной сети