"""API FastAPI que carga una sola vez el clasificador Iris entrenado."""

from contextlib import asynccontextmanager
import os
from pathlib import Path

import joblib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field


MODEL_PATH = Path(__file__).resolve().parents[1] / "modelo" / "modelo.joblib"
DEFAULT_ORIGINS = "http://127.0.0.1:5500,http://localhost:5500"
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", DEFAULT_ORIGINS).split(",")
    if origin.strip()
]
SPECIES = ("setosa", "versicolor", "virginica")


class FlowerMeasurements(BaseModel):
    """Contrato de entrada: las cuatro medidas se expresan en centímetros."""

    model_config = ConfigDict(strict=True)

    sepal_length_cm: float = Field(ge=4.3, le=7.9, description="Largo del sépalo, entre 4.3 y 7.9 cm")
    sepal_width_cm: float = Field(ge=2.0, le=4.4, description="Ancho del sépalo, entre 2.0 y 4.4 cm")
    petal_length_cm: float = Field(ge=1.0, le=6.9, description="Largo del pétalo, entre 1.0 y 6.9 cm")
    petal_width_cm: float = Field(ge=0.1, le=2.5, description="Ancho del pétalo, entre 0.1 y 2.5 cm")


class Prediction(BaseModel):
    especie: str
    probabilidades: dict[str, float]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el archivo una vez al iniciar el proceso del servidor."""
    if not MODEL_PATH.is_file():
        raise RuntimeError(
            f"No encuentro el modelo entrenado en {MODEL_PATH}. "
            "Ejecutá primero el notebook de entrenamiento."
        )
    app.state.model = joblib.load(MODEL_PATH)
    yield


app = FastAPI(
    title="Jardín de Datos: API de Iris",
    description="Clasifica una flor a partir de cuatro medidas en centímetros.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Comprueba que el servidor responde."""
    return {"estado": "ok"}


@app.post("/predecir", response_model=Prediction)
def predict(flower: FlowerMeasurements, request: Request) -> Prediction:
    """Devuelve la especie estimada y las probabilidades del clasificador."""
    values = [[
        flower.sepal_length_cm,
        flower.sepal_width_cm,
        flower.petal_length_cm,
        flower.petal_width_cm,
    ]]
    model = request.app.state.model
    predicted_index = int(model.predict(values)[0])
    raw_probabilities = model.predict_proba(values)[0]
    probabilities = {
        species: float(round(float(probability), 4))
        for species, probability in zip(SPECIES, raw_probabilities)
    }
    return Prediction(
        especie=SPECIES[predicted_index],
        probabilidades=probabilities,
    )
