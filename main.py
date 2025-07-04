from fastapi import FastAPI, Request
from model import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Allow everything (only for development use)
    allow_methods=["*"], 
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