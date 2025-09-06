from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str

def simple_label(t: str) -> str:
    t = t.lower()
    if any(w in t for w in ["http", "buy now", "spam"]):
        return "violation"
    if len(t.strip()) < 5:
        return "low_quality"
    return "high_quality"

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/classify")
def classify(item: Item):
    return {"label": simple_label(item.text)}
