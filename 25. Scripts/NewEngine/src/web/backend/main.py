from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class IHMConfig(BaseModel):
    ihm_type: str
    is_active: bool

@app.get("/")
def read_root():
    return {"Hello": "Paletizador Web Configurator"}

@app.get("/ihm/options")
def get_ihm_options():
    return [
        {"id": "siemens", "label": "Siemens (Padrão)", "image": "siemens_preview.png"},
        {"id": "zenon", "label": "Zenon (Legado)", "image": "zenon_preview.png"},
        {"id": "clearline", "label": "Clearline (Específico)", "image": "clearline_preview.png"}
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
