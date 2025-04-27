from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
async def root():
    return {"Mensagem":"Hello Word!!!!"}


@app.get("/gerarid")
async def root():
    return {"numero Aleatorio":random.randint(10000,99998)}


