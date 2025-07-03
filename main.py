from fastapi import FastAPI
from model import predict

app = FastAPI()

@app.post("/predict")
async def predict_entities(text):
    predict(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Opening for local network