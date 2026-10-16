from functools import lru_cache
import os
from pathlib import Path

import gradio as gr
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F


MODEL_ID = "intfloat/multilingual-e5-small"
TRANSCRIPTION_MODEL_ID = "openai/whisper-tiny"
OFFERS_PATH = Path(__file__).with_name("ofertas.csv")
REQUIRED_COLUMNS = {
    "supermercado",
    "producto",
    "precio",
    "cantidad",
    "unidad",
    "fecha_relevamiento",
    "fuente",
}


def load_offers() -> pd.DataFrame:
    if not OFFERS_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de ofertas: {OFFERS_PATH}")

    offers = pd.read_csv(OFFERS_PATH)
    missing_columns = REQUIRED_COLUMNS.difference(offers.columns)
    if missing_columns:
        raise ValueError(
            "Faltan columnas requeridas en ofertas.csv: "
            + ", ".join(sorted(missing_columns))
        )

    offers["precio"] = pd.to_numeric(offers["precio"], errors="raise")
    offers["cantidad"] = pd.to_numeric(offers["cantidad"], errors="raise")
    if (offers["precio"] <= 0).any() or (offers["cantidad"] <= 0).any():
        raise ValueError("Los precios y las cantidades deben ser mayores que cero.")
    return offers


OFFERS = load_offers()


@lru_cache(maxsize=1)
def load_embedding_model():
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModel.from_pretrained(MODEL_ID)
    model.eval()
    return tokenizer, model


@lru_cache(maxsize=2048)
def embed_text(text: str) -> torch.Tensor:
    tokenizer, model = load_embedding_model()
    tokens = tokenizer(
        f"query: {text}",
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )
    with torch.inference_mode():
        output = model(**tokens)
        attention_mask = tokens["attention_mask"].unsqueeze(-1)
        pooled = (output.last_hidden_state * attention_mask).sum(dim=1)
        pooled = pooled / attention_mask.sum(dim=1).clamp(min=1)
        return F.normalize(pooled, p=2, dim=1)[0]


@lru_cache(maxsize=1)
def load_transcription_pipeline():
    from transformers import pipeline

    return pipeline(
        "automatic-speech-recognition",
        model=TRANSCRIPTION_MODEL_ID,
        device=-1,
    )


def search_offers(query: str) -> tuple[pd.DataFrame, str]:
    query = (query or "").strip()
    if not query:
        return pd.DataFrame(), "Escribí un producto, por ejemplo: leche entera 1 litro."

    query_vector = embed_text(query)
    product_vectors = torch.stack(
        [embed_text(product) for product in OFFERS["producto"].astype(str)]
    )
    scores = (product_vectors @ query_vector).cpu().numpy()
    results = OFFERS.copy()
    results["similitud"] = [round(float(score), 3) for score in scores]
    results = results.nlargest(5, "similitud").copy()

    results["precio_por_100"] = (
        results["precio"] / results["cantidad"] * 100
    ).round(2)
    message = (
        "Se muestran las cinco ofertas con mayor similitud. El score no es una "
        "probabilidad ni confirma que sean el mismo producto: verificá tipo, marca "
        "y cantidad antes de comparar precios."
    )
    columns = [
        "supermercado",
        "producto",
        "precio",
        "cantidad",
        "unidad",
        "precio_por_100",
        "similitud",
        "fecha_relevamiento",
        "fuente",
    ]
    return results[columns], message


def search_from_inputs(
    query: str,
    audio_input: tuple[int, np.ndarray] | None,
) -> tuple[str, pd.DataFrame, str]:
    query = (query or "").strip()
    if audio_input is not None:
        sample_rate, audio_array = audio_input
        audio_array = np.asarray(audio_array)
        if np.issubdtype(audio_array.dtype, np.integer):
            audio_array = audio_array.astype(np.float32) / np.iinfo(
                audio_array.dtype
            ).max
        else:
            audio_array = audio_array.astype(np.float32)
        if audio_array.ndim == 2:
            channel_axis = 0 if audio_array.shape[0] <= 2 else 1
            audio_array = audio_array.mean(axis=channel_axis)
        if audio_array.size == 0 or np.max(np.abs(audio_array)) < 1e-4:
            return "", pd.DataFrame(), (
                "El audio está vacío o demasiado bajo. Probá grabarlo otra vez "
                "o escribí el producto."
            )

        transcription = load_transcription_pipeline()(
            {"raw": audio_array, "sampling_rate": sample_rate},
            generate_kwargs={
                "language": "spanish",
                "task": "transcribe",
                "max_new_tokens": 64,
                "temperature": 0.0,
                "condition_on_prev_tokens": False,
            },
        )

        transcript = transcription["text"].strip()
        if not transcript:
            return "", pd.DataFrame(), (
                "No se reconocieron palabras. Probá hablar más cerca del micrófono "
                "o escribí el producto."
            )
        results, message = search_offers(transcript)
        return transcript, results, message

    if not query:
        return "", pd.DataFrame(), (
            "Escribí el producto o grabá un audio con el botón del micrófono."
        )

    results, message = search_offers(query)
    return query, results, message


demo = gr.Interface(
    fn=search_from_inputs,
    inputs=[
        gr.Textbox(
            label="Escribí un producto (opcional si vas a hablar)",
            placeholder="Ej.: leche entera 1 litro",
        ),
        gr.Audio(
            sources=["microphone", "upload"],
            type="numpy",
            label="O grabá / subí un audio en español",
        ),
    ],
    outputs=[
        gr.Textbox(label="Texto reconocido", interactive=False),
        gr.Dataframe(label="Ofertas similares"),
        gr.Textbox(label="Resultado"),
    ],
    title="Comparador de ofertas",
    description=(
        "Buscá productos aunque la consulta y el nombre de la oferta no coincidan "
        "exactamente. Escribí o grabá el producto; la frase reconocida aparece "
        "antes de los resultados. Los modelos se ejecutan localmente y los datos "
        "incluidos son de demostración."
    ),
)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
    )
