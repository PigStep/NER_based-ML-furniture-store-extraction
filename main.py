from fastapi import FastAPI, Request
from model import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем запросы от любых источников (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретный домен, например "http://localhost:3000"
    allow_methods=["*"],  # Разрешаем все методы, включая OPTIONS
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_entities(request: Request):
    try:
        url = await request.body()
        result = predict(url)
        return {"result": result}
    except Exception as e:
        return e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Opening for local network